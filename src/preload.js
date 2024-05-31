const { contextBridge, ipcRenderer } = require('electron');

// Ana dünya ile güvenli bir şekilde iletişim kurmak için contextBridge kullanıyoruz
contextBridge.exposeInMainWorld('electron', {
  // Ana süreçten popup penceresi açma isteği gönderen fonksiyon
  openPopup: (imageData, textData) => ipcRenderer.send('open-popup', imageData, textData),

  // Ana süreçten gelen görüntü verisini dinleyen fonksiyon
  onDisplayImage: (callback) => ipcRenderer.on('display-image', (event, data) => callback(data)),

  // Ana süreçten gelen metin verisini dinleyen fonksiyon
  onDisplayTextData: (callback) => ipcRenderer.on('display-text-data', (event, data) => callback(data))
});
