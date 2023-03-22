// Detect code function
const detectCode = () => {
    // Start detecting codes on to the video element
    barcodeDetector.detect(video).then(codes => {
        if (codes.length === 0) {
            return;
        }
        for (const barcode of codes)  {
          console.log(barcode);
        }
    }).catch(err => {
        console.error(err);
      })
    }

if (('BarcodeDetector' in window)) {
    const video = document.querySelector('#video')
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      const constraints = {
        video: true,
        audio: false
      }
      navigator.mediaDevices.getUserMedia(constraints).then(stream => video.srcObject = stream);
    }

    let formats;
    // Save all formats to formats var
    BarcodeDetector.getSupportedFormats().then(arr => formats = arr);
    // Create new barcode detector with all supported formats

    // Create new barcode detector
    const barcodeDetector = new BarcodeDetector({ formats: ['ean_13'] });
    // Run detect code function every 100 milliseconds
    setInterval(detectCode, 100);
} else {
    window.location.replace("http://127.0.0.1:8000/account");
}





