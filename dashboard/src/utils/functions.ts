export function handleUpload(e): Promise<string>{
    /**
     * Handling uplading and return the selected file. Tried my best here to apply the single responsibility method.
     * so this function is just doing one job.  
     * @returns the file path (url)
     */
    const file = e.target.files[0]
    if (!file) return Promise.resolve("")

    // Promise is a way like async making sure this step is done before moving to the next one. 
    // Use await to call this function.
    return new Promise((resolve) => {
      const reader = new FileReader()
      reader.onload = (e) => {
        const base64 = e.target?.result as string
        resolve(base64)  // Now it notifying that the process is done. 
      }
      reader.readAsDataURL(file)
    })
    
    // This was is saving the data in memory, it reser when restart.
    // const file = e.target.files[0]
    // if (!file) return '';
    // const url:string = URL.createObjectURL(file)
    // return url
  }

