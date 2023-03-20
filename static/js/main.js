

var input = document.getElementById('img_upl');
var preview = document.querySelector('.preview');

input.style.opacity = 0;

input.addEventListener('change', updateImageDisplay);function updateImageDisplay() {
	while(preview.firstChild) {
		preview.removeChild(preview.firstChild);
	}

	if(input.files.length === 0) {
		var para = document.createElement('p');
		para.textContent = '未選擇任何檔案';
    para.style="line-height: 20em;";
		preview.appendChild(para);
	} 
	else {
		var para = document.createElement('p');
		var image = document.createElement('img');
    image.style='max-width: 100%;max-height: 100%;'
		image.src = window.URL.createObjectURL(input.files[0]);
    
    



		preview.appendChild(image);
		preview.appendChild(para);
	}
}



function Base64Image(file) {
  return new Promise((resolve,reject)=>{
      // 建立FileReader物件
      let reader = new FileReader()
      // 註冊onload事件，取得result則resolve (會是一個Base64字串)
      reader.onload = () => { resolve(reader.result) }
      // 註冊onerror事件，若發生error則reject
      reader.onerror = () => { reject(reader.error) }
      // 讀取檔案
      reader.readAsDataURL(file)
  })
}



function uploadImg(e) {
  // 檔案位置
  var base64 = Base64Image(input.files[0]); 
  base64.then(function(value){
    console.log(value)
    //const formData = new FormData();
    //formData.append('image', "value");
    //console.log(formData)
    let dataJSON={}
    dataJSON["image"]=value

    
    $.ajax({
      type: "POST",
      url: "/upload_img",
      data: JSON.stringify(dataJSON),
      success: (data) => {
        console.log(data.validate);
        console.log(data.img);

        alert(data.validate)
        //也可以用jquery來呈現結果
      },
      dataType: "json",
      contentType: "application/json;charset=utf-8",
    });
  })
  // 新增 formData
  
}

input.addEventListener('change', uploadImg);
