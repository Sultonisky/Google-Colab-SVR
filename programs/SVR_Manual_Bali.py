"""
Program Perhitungan Manual SVR (Support Vector Regression)
"""

import pandas as pd
import numpy as np
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import warnings
import glob
from pathlib import Path
warnings.filterwarnings('ignore')

class SVRForecasting:
    def __init__(self, file_path):
        """
        Inisialisasi dengan path file Excel
        
        Parameters:
        -----------
        file_path : str
            Path ke file Excel yang berisi data occupancy rate
        """
        base_dir = Path(__file__).resolve().parent
        root_dir = base_dir.parent
        self.base_dir = base_dir
        self.root_dir = root_dir
        self.dataset_dir = root_dir / "dataset"
        self.result_dataset_dir = root_dir / "result" / "dataset"
        self.result_img_dir = root_dir / "result" / "img"

        self.file_path = Path(file_path)
        self.data = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler_X = StandardScaler()
        self.scaler_y = StandardScaler()
        self.model = None
        self.manual_svr_results = None  # Untuk menyimpan hasil perhitungan manual
        
    def load_data(self, sheet_name=0):
        """
        Memuat data dari file Excel
        """
        print("=" * 60)
        print("STEP 1: MEMUAT DATA DARI FILE EXCEL")
        print("=" * 60)
        
        try:
            # Membaca file Excel (sheet sesuai parameter)
            self.data = pd.read_excel(self.file_path, sheet_name=sheet_name)
            print(f"\n[SUCCESS] Data loaded successfully!")
            print(f"Number of rows: {len(self.data)}")
            print(f"Number of columns: {len(self.data.columns)}")
            print("\nData preview:")
            print(self.data.head())
            print("\nData info:")
            print(self.data.info())
            print("\nDescriptive statistics:")
            print(self.data.describe())
            
            return True
        except Exception as e:
            print(f"Error saat memuat data: {str(e)}")
            return False
    
    def prepare_features(self, target_column, feature_columns=None, lag_periods=3):
        """
        Menyiapkan fitur untuk analisis/pelatihan (opsional)
        
        Parameters:
        -----------
        target_column : str
            Nama kolom target (mis. occupancy rate)
        feature_columns : list, optional
            Daftar kolom fitur tambahan. Jika None, akan menggunakan lag features
        lag_periods : int
            Jumlah periode lag untuk membuat fitur time series
        """
        print("\n" + "=" * 60)
        print("STEP 2: MENYIAPKAN FITUR (FEATURE PREPARATION)")
        print("=" * 60)
        
        if target_column not in self.data.columns:
            print(f"Error: Kolom '{target_column}' tidak ditemukan!")
            print(f"Kolom yang tersedia: {list(self.data.columns)}")
            return False
        
        # Mengambil target variable
        target = self.data[target_column].values
        
        # Membuat lag features jika feature_columns tidak diberikan
        if feature_columns is None:
            print(f"\nMembuat lag features dengan {lag_periods} periode...")
            lag_features = []
            
            for lag in range(1, lag_periods + 1):
                lag_feature = np.roll(target, lag)
                lag_feature[:lag] = np.nan
                lag_features.append(lag_feature)
            
            # Menggabungkan lag features
            X_data = np.column_stack(lag_features)
            
            # Menghapus baris dengan NaN (karena lag)
            valid_indices = ~np.isnan(X_data).any(axis=1)
            X_data = X_data[valid_indices]
            target = target[valid_indices]
            
            print(f"Jumlah fitur: {lag_periods} (lag features)")
            print(f"Shape X: {X_data.shape}")
            print(f"Shape y: {target.shape}")
            
        else:
            # Menggunakan kolom yang ditentukan
            print(f"\nMenggunakan kolom fitur: {feature_columns}")
            X_data = self.data[feature_columns].values
            target = self.data[target_column].values
            
            # Menghapus baris dengan NaN
            valid_indices = ~np.isnan(X_data).any(axis=1) & ~np.isnan(target)
            X_data = X_data[valid_indices]
            target = target[valid_indices]
        
        self.X = X_data
        self.y = target.reshape(-1, 1)
        
        print(f"\n[SUCCESS] Features prepared successfully!")
        print(f"X shape: {self.X.shape}")
        print(f"y shape: {self.y.shape}")
        
        return True
    
    def split_data(self, test_size=0.2, random_state=42):
        """
        Membagi data menjadi training dan testing set
        
        Parameters:
        -----------
        test_size : float
            Proporsi data testing (default: 0.2 = 20%)
        random_state : int
            Random seed untuk reproducibility
        """
        print("\n" + "=" * 60)
        print("STEP 3: MEMBAGI DATA (TRAIN-TEST SPLIT)")
        print("=" * 60)
        
        # Untuk time series, lebih baik menggunakan split berurutan
        split_idx = int(len(self.X) * (1 - test_size))
        
        self.X_train = self.X[:split_idx]
        self.X_test = self.X[split_idx:]
        self.y_train = self.y[:split_idx]
        self.y_test = self.y[split_idx:]
        
        print(f"\nData Training:")
        print(f"  X_train shape: {self.X_train.shape}")
        print(f"  y_train shape: {self.y_train.shape}")
        print(f"\nData Testing:")
        print(f"  X_test shape: {self.X_test.shape}")
        print(f"  y_test shape: {self.y_test.shape}")
        print(f"\nProporsi: {len(self.X_train)/len(self.X)*100:.1f}% training, {len(self.X_test)/len(self.X)*100:.1f}% testing")
        
    def scale_data(self):
        """
        Normalisasi data menggunakan StandardScaler
        """
        print("\n" + "=" * 60)
        print("STEP 4: NORMALISASI DATA (SCALING)")
        print("=" * 60)
        
        print("\nSebelum scaling:")
        print(f"  X_train - Mean: {self.X_train.mean(axis=0)}, Std: {self.X_train.std(axis=0)}")
        print(f"  y_train - Mean: {self.y_train.mean()}, Std: {self.y_train.std()}")
        
        # Scaling fitur X
        self.X_train = self.scaler_X.fit_transform(self.X_train)
        self.X_test = self.scaler_X.transform(self.X_test)
        
        # Scaling target y
        self.y_train = self.scaler_y.fit_transform(self.y_train).ravel()
        self.y_test = self.scaler_y.transform(self.y_test).ravel()
        
        print("\nAfter scaling:")
        print(f"  X_train - Mean: {self.X_train.mean(axis=0)}, Std: {self.X_train.std(axis=0)}")
        print(f"  y_train - Mean: {self.y_train.mean():.6f}, Std: {self.y_train.std():.6f}")
        print("\n[SUCCESS] Data normalized successfully!")
    
    def train_model(self, kernel='rbf', C=100, gamma='scale', epsilon=0.1):
        """
        Melatih model SVR
        
        Parameters:
        -----------
        kernel : str
            Jenis kernel ('rbf', 'linear', 'poly', 'sigmoid')
        C : float
            Parameter regularisasi (default: 100)
        gamma : str or float
            Parameter kernel coefficient (default: 'scale')
        epsilon : float
            Epsilon-tube untuk loss function (default: 0.1)
        """
        print("\n" + "=" * 60)
        print("STEP 5: MELATIH MODEL SVR")
        print("=" * 60)
        
        print(f"\nParameter SVR:")
        print(f"  Kernel: {kernel}")
        print(f"  C (Regularization): {C}")
        print(f"  Gamma: {gamma}")
        print(f"  Epsilon: {epsilon}")
        
        # Membuat model SVR
        self.model = SVR(kernel=kernel, C=C, gamma=gamma, epsilon=epsilon)
        
        print("\nStarting training...")
        self.model.fit(self.X_train, self.y_train)
        
        print("[SUCCESS] Training completed!")
        print(f"Number of support vectors: {len(self.model.support_)}")
        print(f"Support vectors per class: {self.model.n_support_}")
        
    def evaluate_model(self):
        """
        Mengevaluasi performa model
        """
        print("\n" + "=" * 60)
        print("STEP 6: EVALUASI MODEL")
        print("=" * 60)
        
        # Prediksi pada data training
        y_train_pred = self.model.predict(self.X_train)
        y_train_pred = self.scaler_y.inverse_transform(y_train_pred.reshape(-1, 1)).ravel()
        y_train_actual = self.scaler_y.inverse_transform(self.y_train.reshape(-1, 1)).ravel()
        
        # Prediksi pada data testing
        y_test_pred = self.model.predict(self.X_test)
        y_test_pred = self.scaler_y.inverse_transform(y_test_pred.reshape(-1, 1)).ravel()
        y_test_actual = self.scaler_y.inverse_transform(self.y_test.reshape(-1, 1)).ravel()
        
        # Menghitung metrik untuk training
        train_mse = mean_squared_error(y_train_actual, y_train_pred)
        train_rmse = np.sqrt(train_mse)
        train_mae = mean_absolute_error(y_train_actual, y_train_pred)
        train_r2 = r2_score(y_train_actual, y_train_pred)
        
        # Menghitung metrik untuk testing
        test_mse = mean_squared_error(y_test_actual, y_test_pred)
        test_rmse = np.sqrt(test_mse)
        test_mae = mean_absolute_error(y_test_actual, y_test_pred)
        test_r2 = r2_score(y_test_actual, y_test_pred)
        
        print("\nHasil Evaluasi - Data Training:")
        print(f"  MSE (Mean Squared Error): {train_mse:.4f}")
        print(f"  RMSE (Root Mean Squared Error): {train_rmse:.4f}")
        print(f"  MAE (Mean Absolute Error): {train_mae:.4f}")
        print(f"  R² Score: {train_r2:.4f}")
        
        print("\nHasil Evaluasi - Data Testing:")
        print(f"  MSE (Mean Squared Error): {test_mse:.4f}")
        print(f"  RMSE (Root Mean Squared Error): {test_rmse:.4f}")
        print(f"  MAE (Mean Absolute Error): {test_mae:.4f}")
        print(f"  R² Score: {test_r2:.4f}")
        
        return {
            'train': {'mse': train_mse, 'rmse': train_rmse, 'mae': train_mae, 'r2': train_r2},
            'test': {'mse': test_mse, 'rmse': test_rmse, 'mae': test_mae, 'r2': test_r2},
            'y_train_actual': y_train_actual,
            'y_train_pred': y_train_pred,
            'y_test_actual': y_test_actual,
            'y_test_pred': y_test_pred
        }
    
    def visualize_results(self, eval_results):
        """
        Visualisasi hasil pelatihan/prediksi historis (jika digunakan)
        """
        print("\n" + "=" * 60)
        print("VISUALISASI HASIL")
        print("=" * 60)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Plot 1: Training Data
        axes[0, 0].plot(eval_results['y_train_actual'], label='Actual', marker='o', markersize=3)
        axes[0, 0].plot(eval_results['y_train_pred'], label='Predicted', marker='s', markersize=3)
        axes[0, 0].set_title('Training Data: Actual vs Predicted')
        axes[0, 0].set_xlabel('Periode')
        axes[0, 0].set_ylabel('Occupancy Rate')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Testing Data
        axes[0, 1].plot(eval_results['y_test_actual'], label='Actual', marker='o', markersize=3)
        axes[0, 1].plot(eval_results['y_test_pred'], label='Predicted', marker='s', markersize=3)
        axes[0, 1].set_title('Testing Data: Actual vs Predicted')
        axes[0, 1].set_xlabel('Periode')
        axes[0, 1].set_ylabel('Occupancy Rate')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Scatter Plot Training
        axes[1, 0].scatter(eval_results['y_train_actual'], eval_results['y_train_pred'], alpha=0.5)
        min_val = min(eval_results['y_train_actual'].min(), eval_results['y_train_pred'].min())
        max_val = max(eval_results['y_train_actual'].max(), eval_results['y_train_pred'].max())
        axes[1, 0].plot([min_val, max_val], [min_val, max_val], 'r--', lw=2)
        axes[1, 0].set_xlabel('Actual')
        axes[1, 0].set_ylabel('Predicted')
        axes[1, 0].set_title(f'Training: R² = {eval_results["train"]["r2"]:.4f}')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Scatter Plot Testing
        axes[1, 1].scatter(eval_results['y_test_actual'], eval_results['y_test_pred'], alpha=0.5)
        min_val = min(eval_results['y_test_actual'].min(), eval_results['y_test_pred'].min())
        max_val = max(eval_results['y_test_actual'].max(), eval_results['y_test_pred'].max())
        axes[1, 1].plot([min_val, max_val], [min_val, max_val], 'r--', lw=2)
        axes[1, 1].set_xlabel('Actual')
        axes[1, 1].set_ylabel('Predicted')
        axes[1, 1].set_title(f'Testing: R² = {eval_results["test"]["r2"]:.4f}')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        self.result_img_dir.mkdir(parents=True, exist_ok=True)
        img_path = self.result_img_dir / 'SVR_Manual_Bali_results.png'
        plt.savefig(img_path, dpi=300, bbox_inches='tight')
        print(f"\n[SUCCESS] Visualization saved as '{img_path}'")
        plt.show()
    
    
    
    def find_columns(self, possible_names):
        """
        Mencari kolom berdasarkan beberapa kemungkinan nama
        
        Parameters:
        -----------
        possible_names : list
            Daftar nama kolom yang mungkin
            
        Returns:
        --------
        str or None: Nama kolom yang ditemukan, atau None jika tidak ada
        """
        for name in possible_names:
            # Cek exact match
            if name in self.data.columns:
                return name
            # Cek case-insensitive
            for col in self.data.columns:
                if col.lower() == name.lower():
                    return col
            # Cek partial match
            for col in self.data.columns:
                if name.lower() in col.lower() or col.lower() in name.lower():
                    return col
        return None
    def calculate_manual_svr(self, rooms_sold_col=None, rooms_available_col=None, 
                            w1=0.01152, w2=-0.000843, b=0.02091, 
                            output_col='X', n_rows=10):
        """
        Menghitung SVR secara manual menggunakan formula linear
        
        Formula: y = w1 * rooms_sold + w2 * rooms_available + b
        
        Parameters:
        -----------
        rooms_sold_col : str, optional
            Nama kolom untuk rooms_sold. Jika None, akan dicari otomatis
        rooms_available_col : str, optional
            Nama kolom untuk rooms_available. Jika None, akan dicari otomatis
        w1 : float
            Bobot untuk rooms_sold (default: 0.01152)
        w2 : float
            Bobot untuk rooms_available (default: -0.000843)
        b : float
            Bias/intercept (default: 0.02091)
        output_col : str
            Nama kolom output untuk menyimpan hasil (default: 'X')
        n_rows : int
            Jumlah baris pertama yang akan ditampilkan perhitungannya (default: 10)
        """
        print("\n" + "=" * 60)
        print("PERHITUNGAN MANUAL SVR DENGAN KERNEL LINEAR")
        print("=" * 60)
        
        # Auto-detect kolom jika tidak diberikan
        if rooms_sold_col is None:
            rooms_sold_col = self.find_columns([
                'rooms_sold', 'room_sold', 'sold', 'rooms_sold_count',
                'jumlah_kamar_terjual', 'kamar_terjual'
            ])
        
        if rooms_available_col is None:
            rooms_available_col = self.find_columns([
                'rooms_available', 'room_available', 'available', 
                'rooms_available_count', 'jumlah_kamar_tersedia', 'kamar_tersedia'
            ])
        
        # Validasi kolom
        if rooms_sold_col is None or rooms_sold_col not in self.data.columns:
            print(f"\n[ERROR] Column 'rooms_sold' not found!")
            print(f"Available columns: {list(self.data.columns)}")
            print(f"\nPlease specify column name manually:")
            print(f"  forecaster.calculate_manual_svr(")
            print(f"      rooms_sold_col='your_rooms_sold_column',")
            print(f"      rooms_available_col='your_rooms_available_column'")
            print(f"  )")
            return False
        
        if rooms_available_col is None or rooms_available_col not in self.data.columns:
            print(f"\n[ERROR] Column 'rooms_available' not found!")
            print(f"Available columns: {list(self.data.columns)}")
            print(f"\nPlease specify column name manually:")
            print(f"  forecaster.calculate_manual_svr(")
            print(f"      rooms_sold_col='your_rooms_sold_column',")
            print(f"      rooms_available_col='your_rooms_available_column'")
            print(f"  )")
            return False
        
        print(f"\nColumns used:")
        print(f"  rooms_sold: '{rooms_sold_col}'")
        print(f"  rooms_available: '{rooms_available_col}'")
        
        print(f"\nLinear SVR Formula:")
        print(f"  y = w1 * {rooms_sold_col} + w2 * {rooms_available_col} + b")
        print(f"\nParameters:")
        print(f"  w1 (rooms_sold weight)     = {w1}")
        print(f"  w2 (rooms_available weight) = {w2}")
        print(f"  b (bias/intercept)         = {b}")
        
        # Mengambil data
        rooms_sold = self.data[rooms_sold_col].values
        rooms_available = self.data[rooms_available_col].values
        
        # Menghitung SVR secara manual
        svr_results = w1 * rooms_sold + w2 * rooms_available + b
        
        # Menyimpan hasil ke dataframe
        self.data[output_col] = svr_results
        self.manual_svr_results = svr_results
        
        print(f"\n{'='*60}")
        print(f"STEP-BY-STEP CALCULATION (FIRST 10 ROWS)")
        print(f"{'='*60}")
        print(f"\n{'No':<5} {rooms_sold_col:<15} {rooms_available_col:<20} {'Calculation':<40} {'Result (X)':<15}")
        print("-" * 95)
        
        for i in range(min(n_rows, len(self.data))):
            rs = rooms_sold[i]
            ra = rooms_available[i]
            calc_str = f"{w1} × {rs:.2f} + {w2} × {ra:.2f} + {b}"
            result = svr_results[i]
            print(f"{i+1:<5} {rs:<15.2f} {ra:<20.2f} {calc_str:<40} {result:<15.6f}")
        
        if len(self.data) > n_rows:
            print(f"\n... (total {len(self.data)} baris)")
        
        print(f"\n{'='*60}")
        print(f"MANUAL SVR CALCULATION SUMMARY")
        print(f"{'='*60}")
        print(f"Total rows calculated: {len(svr_results)}")
        print(f"Minimum value: {svr_results.min():.6f}")
        print(f"Maximum value: {svr_results.max():.6f}")
        print(f"Average value: {svr_results.mean():.6f}")
        print(f"Standard deviation: {svr_results.std():.6f}")
        print(f"\n[SUCCESS] Results saved to column '{output_col}' in dataframe!")
        
        return True
    
    def explain_svr_calculation(self):
        """
        Menjelaskan perhitungan SVR secara detail
        """
        print("\n" + "=" * 60)
        print("PENJELASAN PERHITUNGAN SVR (SUPPORT VECTOR REGRESSION)")
        print("=" * 60)
        
        explanation = """
1) Rumus inti (kernel linear)
   y = (w1 * rooms_sold) + (w2 * rooms_available) + b
   Dipakai apa adanya (tanpa scaling), sesuai parameter yang diberikan.

2) Parameter yang digunakan
   - w1 = 0.01152   → pengaruh rooms_sold (positif)
   - w2 = -0.000843 → pengaruh rooms_available (negatif)
   - b  = 0.02091   → bias/intercept (baseline saat fitur = 0)

3) Contoh perhitungan (langkah eksplisit)
   Misal rooms_sold = 100, rooms_available = 200:
   a. Kontribusi rooms_sold:      0.01152 * 100  = 1.15200
   b. Kontribusi rooms_available: -0.000843 * 200 = -0.16860
   c. Tambahkan bias:             +0.02091
   d. Total: y = 1.15200 - 0.16860 + 0.02091 = 1.00431

4) Interpretasi cepat
   - w1 positif: rooms_sold naik → prediksi naik.
   - w2 negatif: rooms_available naik → prediksi turun (lebih banyak kamar kosong).
   - b sebagai baseline jika semua fitur 0; pada data nyata biasanya y bergantung pada skala fitur.

5) Kenapa linear?
   - Asumsi hubungan cukup linear, perhitungan cepat, mudah dijelaskan, dan selaras dengan parameter yang sudah ditetapkan.
        """
        
        print(explanation)
        print("\n" + "=" * 60)
    
    def visualize_manual_svr_results(self, x_col='X', rooms_sold_col=None, rooms_available_col=None):
        """
        Visualisasi hasil perhitungan manual SVR (kolom X)
        
        Parameters:
        -----------
        x_col : str
            Nama kolom hasil SVR manual (default: 'X')
        rooms_sold_col : str, optional
            Nama kolom rooms_sold untuk visualisasi. Jika None, akan dicari otomatis
        rooms_available_col : str, optional
            Nama kolom rooms_available untuk visualisasi. Jika None, akan dicari otomatis
        """
        print("\n" + "=" * 60)
        print("VISUALISASI HASIL PERHITUNGAN MANUAL SVR")
        print("=" * 60)
        
        if self.data is None:
            print("[ERROR] Data is not loaded.")
            return False
        
        if x_col not in self.data.columns:
            print(f"[ERROR] Column '{x_col}' not found in dataset.")
            print(f"Available columns: {list(self.data.columns)}")
            return False
        
        # Auto-detect kolom jika tidak diberikan
        if rooms_sold_col is None:
            rooms_sold_col = self.find_columns([
                'rooms_sold', 'room_sold', 'sold', 'rooms_sold_count',
                'jumlah_kamar_terjual', 'kamar_terjual'
            ])
        
        if rooms_available_col is None:
            rooms_available_col = self.find_columns([
                'rooms_available', 'room_available', 'available', 
                'rooms_available_count', 'jumlah_kamar_tersedia', 'kamar_tersedia'
            ])
        
        # Ambil data
        x_values = self.data[x_col].values
        indices = np.arange(len(x_values))
        
        # Buat figure dengan 4 subplot
        fig = plt.figure(figsize=(16, 12))
        
        # Plot 1: Time Series - Nilai X seiring waktu
        ax1 = plt.subplot(2, 2, 1)
        ax1.plot(indices, x_values, marker='o', markersize=3, linewidth=1.5, color='#2E86AB', label='SVR Manual (X)')
        ax1.axhline(y=x_values.mean(), color='r', linestyle='--', linewidth=2, label=f'Mean: {x_values.mean():.4f}')
        ax1.fill_between(indices, x_values.mean() - x_values.std(), 
                         x_values.mean() + x_values.std(), 
                         alpha=0.2, color='gray', label=f'±1 Std Dev')
        ax1.set_title('Time Series: Hasil Perhitungan Manual SVR (X)', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Periode (Index)', fontsize=10)
        ax1.set_ylabel('Nilai X (SVR Manual)', fontsize=10)
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Histogram/Distribution - Distribusi nilai X
        ax2 = plt.subplot(2, 2, 2)
        n, bins, patches = ax2.hist(x_values, bins=30, edgecolor='black', alpha=0.7, color='#A23B72')
        x_mean = np.mean(x_values)
        x_median = np.median(x_values)
        ax2.axvline(x=x_mean, color='r', linestyle='--', linewidth=2, label=f'Mean: {x_mean:.4f}')
        ax2.axvline(x=x_median, color='g', linestyle='--', linewidth=2, label=f'Median: {x_median:.4f}')
        ax2.set_title('Distribusi Nilai X (SVR Manual)', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Nilai X', fontsize=10)
        ax2.set_ylabel('Frekuensi', fontsize=10)
        ax2.legend(loc='best')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Plot 3: Scatter Plot - Hubungan rooms_sold vs X
        if rooms_sold_col and rooms_sold_col in self.data.columns:
            ax3 = plt.subplot(2, 2, 3)
            rooms_sold = self.data[rooms_sold_col].values
            # Hapus NaN untuk plotting
            mask = ~(np.isnan(rooms_sold) | np.isnan(x_values))
            ax3.scatter(rooms_sold[mask], x_values[mask], alpha=0.6, color='#F18F01', s=50)
            
            # Fit linear trend line
            if np.sum(mask) > 1:
                z = np.polyfit(rooms_sold[mask], x_values[mask], 1)
                p = np.poly1d(z)
                ax3.plot(rooms_sold[mask], p(rooms_sold[mask]), "r--", alpha=0.8, linewidth=2, 
                        label=f'Trend: y={z[0]:.6f}x+{z[1]:.4f}')
            
            ax3.set_title(f'Hubungan {rooms_sold_col} vs X', fontsize=12, fontweight='bold')
            ax3.set_xlabel(f'{rooms_sold_col}', fontsize=10)
            ax3.set_ylabel('Nilai X (SVR Manual)', fontsize=10)
            ax3.legend(loc='best')
            ax3.grid(True, alpha=0.3)
        else:
            ax3 = plt.subplot(2, 2, 3)
            ax3.text(0.5, 0.5, 'Data rooms_sold tidak tersedia', 
                    ha='center', va='center', fontsize=12, transform=ax3.transAxes)
            ax3.set_title('Hubungan rooms_sold vs X', fontsize=12, fontweight='bold')
        
        # Plot 4: Scatter Plot - Hubungan rooms_available vs X
        if rooms_available_col and rooms_available_col in self.data.columns:
            ax4 = plt.subplot(2, 2, 4)
            rooms_available = self.data[rooms_available_col].values
            # Hapus NaN untuk plotting
            mask = ~(np.isnan(rooms_available) | np.isnan(x_values))
            ax4.scatter(rooms_available[mask], x_values[mask], alpha=0.6, color='#C73E1D', s=50)
            
            # Fit linear trend line
            if np.sum(mask) > 1:
                z = np.polyfit(rooms_available[mask], x_values[mask], 1)
                p = np.poly1d(z)
                ax4.plot(rooms_available[mask], p(rooms_available[mask]), "r--", alpha=0.8, linewidth=2,
                        label=f'Trend: y={z[0]:.6f}x+{z[1]:.4f}')
            
            ax4.set_title(f'Hubungan {rooms_available_col} vs X', fontsize=12, fontweight='bold')
            ax4.set_xlabel(f'{rooms_available_col}', fontsize=10)
            ax4.set_ylabel('Nilai X (SVR Manual)', fontsize=10)
            ax4.legend(loc='best')
            ax4.grid(True, alpha=0.3)
        else:
            ax4 = plt.subplot(2, 2, 4)
            ax4.text(0.5, 0.5, 'Data rooms_available tidak tersedia', 
                    ha='center', va='center', fontsize=12, transform=ax4.transAxes)
            ax4.set_title('Hubungan rooms_available vs X', fontsize=12, fontweight='bold')
        
        # Tambahkan statistik di title figure
        stats_text = f"Statistik X: Min={x_values.min():.4f}, Max={x_values.max():.4f}, Mean={x_values.mean():.4f}, Std={x_values.std():.4f}"
        fig.suptitle('Visualisasi Hasil Perhitungan Manual SVR (Bali)\n' + stats_text, 
                    fontsize=14, fontweight='bold', y=0.995)
        
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        
        # Simpan gambar
        self.result_img_dir.mkdir(parents=True, exist_ok=True)
        img_path = self.result_img_dir / 'SVR_Manual_Bali_visualization.png'
        plt.savefig(img_path, dpi=300, bbox_inches='tight')
        print(f"\n[SUCCESS] Visualization saved as '{img_path}'")
        print(f"\nStatistik Nilai X:")
        print(f"  Minimum:  {x_values.min():.6f}")
        print(f"  Maximum:  {x_values.max():.6f}")
        print(f"  Mean:     {x_values.mean():.6f}")
        print(f"  Median:   {np.median(x_values):.6f}")
        print(f"  Std Dev:  {x_values.std():.6f}")
        print(f"  Total:    {len(x_values)} data points")
        
        plt.show()
        return True


def main():
    """
    Fungsi utama untuk menjalankan program
    """
    print("\n" + "=" * 60)
    print("PROGRAM PERHITUNGAN MANUAL SVR (BALI)")
    print("=" * 60)
    
    # Path file Excel (hanya sheet pertama)
    base_dir = Path(__file__).resolve().parent
    root_dir = base_dir.parent
    file_path = root_dir / 'dataset' / 'dataset_bali_2017_2025.xlsx'
    
    # Inisialisasi
    forecaster = SVRForecasting(file_path)
    
    # Step 1: Load data (sheet 1)
    if not forecaster.load_data(sheet_name=0):
        print("\n[ERROR] Failed to load data. Please ensure Excel file exists, sheet 1 is available, and format is correct.")
        return
    
    # ============================================================
    # PART 1: MANUAL SVR CALCULATION (According to Reference)
    # ============================================================
    print("\n" + "=" * 60)
    print("PART 1: MANUAL SVR LINEAR CALCULATION")
    print("=" * 60)
    
    # Check available columns
    print(f"\nAvailable columns in dataset: {list(forecaster.data.columns)}")
    
    # Parameter SVR sesuai referensi
    w1 = 0.01152
    w2 = -0.000843
    b = 0.02091
    
    # Calculate manual SVR (auto-detect columns)
    # Jika kolom tidak ditemukan otomatis, bisa tentukan manual:
    # forecaster.calculate_manual_svr(
    #     rooms_sold_col='your_rooms_sold_column',
    #     rooms_available_col='your_rooms_available_column',
    #     w1=w1, w2=w2, b=b, output_col='X', n_rows=10
    # )
    calculation_ok = forecaster.calculate_manual_svr(
        rooms_sold_col=None,  # Auto-detect
        rooms_available_col=None,  # Auto-detect
        w1=w1, w2=w2, b=b,
        output_col='X',
        n_rows=10
    )
    
    if calculation_ok:
        # Show explanation
        forecaster.explain_svr_calculation()
        
        # Visualisasi hasil perhitungan manual SVR
        print("\n" + "=" * 60)
        print("GENERATING VISUALIZATION...")
        print("=" * 60)
        forecaster.visualize_manual_svr_results(
            x_col='X',
            rooms_sold_col=None,  # Auto-detect
            rooms_available_col=None  # Auto-detect
        )
        
        # Save results to Excel (optional)
        try:
            from datetime import datetime
            
            # Create file name with timestamp to avoid conflict
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            forecaster.result_dataset_dir.mkdir(parents=True, exist_ok=True)
            output_file = forecaster.result_dataset_dir / f'dataset_bali_with_svr_{timestamp}.xlsx'
            
            # Coba simpan
            forecaster.data.to_excel(output_file, index=False)
            print(f"\n[SUCCESS] Dataset with SVR results saved to '{output_file}'")
        except PermissionError:
            print(f"\n[ERROR] Excel file is currently open. Please close the Excel file and try again.")
            print(f"   Attempting to save with different name...")
            try:
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = forecaster.result_dataset_dir / f'SVR_Manual_Bali_dataset_{timestamp}.xlsx'
                forecaster.data.to_excel(output_file, index=False)
                print(f"[SUCCESS] Saved successfully to '{output_file}'")
            except Exception as e2:
                print(f"[ERROR] Still failed: {str(e2)}")
                print(f"   Data remains in memory and can be accessed via forecaster.data")
        except Exception as e:
            print(f"\n[NOTE] Cannot save to Excel: {str(e)}")
            print(f"   Data remains in memory and can be accessed via forecaster.data")
    
    # Selesai: hanya perhitungan manual SVR dan penyimpanan hasil
    print("\n" + "=" * 60)
    print("PROGRAM COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print(f"Hasil SVR manual (kolom 'X') telah disimpan ke result dataset.")
    print("=" * 60)


if __name__ == "__main__":
    main()

# Alias for backward compatibility
SVRManual = SVRForecasting
