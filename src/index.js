const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('node:path');

if (require('electron-squirrel-startup')) {
  app.quit();
}

let popupWindow;

// Ana pencereyi oluşturma fonksiyonu
const createWindow = () => {
  // Ana pencereyi oluşturuyoruz
  const mainWindow = new BrowserWindow({
    width: 1100, // Pencere genişliği
    height: 900, // Pencere yüksekliği
    autoHideMenuBar: true, // Menü çubuğunu otomatik gizler
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'), // Preload betiği
      contextIsolation: true, // Bağlam izolasyonu
      enableRemoteModule: false, // Uzak modül kullanımını devre dışı bırakma
      nodeIntegration: false // Node entegrasyonunu devre dışı bırakma
    },
  });

  // Ana pencereyi yükleme
  mainWindow.loadFile(path.join(__dirname, 'index.html'));

  // Popup penceresini açma ve görüntü verilerini gönderme olayını ele alma
  ipcMain.on('open-popup', (event, imageData, textData) => {
    // Popup penceresini oluşturma
    popupWindow = new BrowserWindow({
      width: 700, // Popup pencere genişliği
      height: 690, // Popup pencere yüksekliği
      autoHideMenuBar: true, // Menü çubuğunu otomatik gizler
      webPreferences: {
        preload: path.join(__dirname, 'preload.js'), // Preload betiği
      },
    });

    // Popup penceresini yükleme
    popupWindow.loadFile(path.join(__dirname, 'popup.html'));
    // Popup penceresi yükleme işlemi tamamlandığında verileri gönderme
    popupWindow.webContents.once('did-finish-load', () => {
      popupWindow.webContents.send('display-image', imageData); // Görüntü verisini gönderme
      popupWindow.webContents.send('display-text-data', textData); // Metin verisini gönderme
    });
  });
};

// Uygulama hazır olduğunda ana pencereyi oluşturma
app.whenReady().then(() => {
  createWindow();

  // Tüm pencereler kapandığında uygulamayı tekrar açma işlemi
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow(); // Eğer açık pencere yoksa yeni bir pencere oluşturur
    }
  });
});

// Tüm pencereler kapandığında uygulamayı kapatma işlemi
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') { // MacOS harici platformlarda
    app.quit(); // Uygulamayı kapatır
  }
});