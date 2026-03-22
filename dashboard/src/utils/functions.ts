export function handleUpload(e): string{
    /**
     * Handling uplading and return the selected file. Tried my best here to apply the single responsibility method.
     * so this function is just doing one job.  
     * @returns the file path (url)
     */
    const file = e.target.files[0]
    if (!file) return '';
    const url:string = URL.createObjectURL(file)
    return url
  }

