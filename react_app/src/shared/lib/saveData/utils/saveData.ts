export const saveData = (function () {
    let downloadEl = document.createElement("a");

    return function (blob: Blob, fileName: string) {
        let url: string = window.URL.createObjectURL(blob);
        downloadEl.href = url;
        downloadEl.download = fileName;
        downloadEl.click();
        window.URL.revokeObjectURL(url);
    };
}());
