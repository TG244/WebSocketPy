"use strict";

var imgLoader = {
    webSocket: null,
    wsSrv: 'ws://localhost:60000',

    width: 640,
    height: 480,

    isJpeg: true,

    onLoad: function() {
        this.webSocket = new WebSocket(this.wsSrv);
        this.webSocket.binaryType = 'arraybuffer';
        this.webSocket.onmessage = imgLoader.onMessage.bind(this);
    },

    onButtonClicked: function() {
        this.webSocket.send('START');
    },

    onMessage: function(data) {
        var img       = new Uint8Array(data.data);
        var canvas    = document.getElementById('canvas');
        var ctx       = canvas.getContext('2d');

        console.log("recv data...");

        if (this.isJpeg) {
            // var image = new Image();
            // image.src = 'data:image/jpeg;base64,' + window.btoa(String.fromCharCode.apply(null, img));
            // image.onload = function() {
            //     ctx.drawImage(image, 0, 0);
            // }

            // 受信したバイナリデータをBlobに変換
            const blob = new Blob([img], { type: "image/jpeg" });
            const url = URL.createObjectURL(blob); // BlobをURLに変換

            const image = new Image();
            image.onload = function () {
                ctx.drawImage(image, 0, 0); // Canvasに描画
                URL.revokeObjectURL(url); // メモリ解放
            };
            image.src = url; // BlobのURLをImageのソースに設定

        } else {
            var imageData = ctx.createImageData(this.width, this.height);

            for (var i = 0; i < imageData.data.length; i++) {
                imageData.data[i] = img[i];
            }
            ctx.putImageData(imageData, 0, 0);
        }
    }
};
