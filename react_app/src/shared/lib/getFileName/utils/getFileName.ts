export const getFileName = (response: Response) => {
    const header = response.headers.get('Content-Disposition');
    const parts = header?.split(';');
    const fileName = parts?.[1].split('=')[1];

    return fileName
}