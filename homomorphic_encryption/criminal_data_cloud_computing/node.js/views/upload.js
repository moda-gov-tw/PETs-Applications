window.addEventListener('load',()=>{
    let selected = document.getElementById("myComboBox");
    selected.selectedIndex = 0;
    let submitButton = document.getElementById("upload");
    let downloadButton = document.getElementById("downloadBtn");
    submitButton.disabled = true;
    downloadButton.disabled = true;
    submitButton.addEventListener('click', () => {
        let selectedValue = document.getElementById("myComboBox").value;
        let downloadBtn = document.getElementById("downloadBtn")
        let fileInput3 = document.getElementById("fileInput3");
        const loadingMask = document.getElementById("loading-mask")
        loadingMask.style.display = 'flex'
        let is_fileinput3 = false;
        if(fileInput3.files.length > 0)
        {
          is_fileinput3 = true;
        }
        else
        {
          is_fileinput3 = false;
        }
        console.log(is_fileinput3);
        let formData = new FormData(document.getElementById("form"));
        formData.append("select",selectedValue);
        formData.append("is_fileinput3",is_fileinput3);
        $.ajax({
            url:"/uploads",
            method:"post",
            contentType:false,
            processData:false,
            data:formData,
            success:function(res){
              loadingMask.style.display = 'none'
              alert(res.message);
              downloadBtn.disabled = false;
              if(selectedValue == "insert")
              {
                downloadBtn.disabled = true;
              }
              
            },
            error:function(xhr, status, error){
              loadingMask.style.display = 'none'
              let response = JSON.parse(xhr.responseText);
              console.log("xhr.responseText:",xhr.responseText);
              alert(response.error);
              downloadBtn.disabled = true;
            },
            xhr: () => {
              const progressBar = document.getElementById("bar")
              const text = document.getElementById("text")
              const xhr = new window.XMLHttpRequest();
              xhr.upload.addEventListener("progress", (event) => {
                if(event.lengthComputable) {
                  const percent = Math.floor((event.loaded / event.total) * 100)  + "%"
                  progressBar.style.width = percent
                  text.innerText = percent
                  console.log(percent) 
                  if(percent == "100%")
                  {
                    text.innerText = "Executing..."
                  }
                }
              }, false)
              return xhr
            }
        })
        
      });
})

    