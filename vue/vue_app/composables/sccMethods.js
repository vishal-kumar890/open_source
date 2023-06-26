const config = useRuntimeConfig()
var server_url = config.public.server_url;

const btn_class =   { 
    customClass:    {
                        confirmButton: 'btn btn-dark',
                        cancelButton: 'btn btn-danger'
                    },
    buttonsStyling: false,
    reverseButtons: true,
    confirmButtonText: "OK",
    cancelButtonText: 'Cancel',
    showCancelButton: false
}

export async function postData(url = '', data = {}) {
    const response = await fetch(server_url+url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        mode: 'cors', // no-cors, *cors, same-origin
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'include', // include, *same-origin, omit
        headers: {
            'Content-Type': 'application/json',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
        body: JSON.stringify(data) // body data type must match "Content-Type" header
    });
    if (response.status == 200) {
        if (response.headers.get('Content-Type') == 'application/json') {
            return response.json(); // parses JSON response into native JavaScript objects
        } else {
            let blobType = response.headers.get('Content-Type')
            let file_name = response.headers.get('Content-Disposition').split("filename=")[1].slice(0, -1)
            response.blob().then(blob_obj => downloadFile(blob_obj, file_name, blobType))
            console.log('content type not application/json')

        }
    }else if (response.status == 401) {
        sessionStorage.clear()
        return navigateTo('/')
    }else {
        let val = await response.text()
        // confirmBox("Error!", val)
        confirmBox("Oops!", val)
        document.querySelectorAll('.modal-preloader').forEach(a=>a.style.display = "none");
        return Promise.reject(new Error(val))
    }
}

export function downloadFile(blob, filename, blobType) {
    // It is necessary to create a new blob object with mime-type explicitly set
    // otherwise only Chrome works like it should
    var newBlob = new Blob([blob], { type: blobType })

    // IE doesn't allow using a blob object directly as link href
    // instead it is necessary to use msSaveOrOpenBlob
    if (window.navigator && window.navigator.msSaveOrOpenBlob) {
        window.navigator.msSaveOrOpenBlob(newBlob);
        return;
    }

    // For other browsers: 
    // Create a link pointing to the ObjectURL containing the blob.
    const data = window.URL.createObjectURL(newBlob);
    var link = document.createElement('a');
    link.href = data;
    link.download = filename;
    link.click();
    setTimeout(function () {
        // For Firefox it is necessary to delay revoking the ObjectURL
        window.URL.revokeObjectURL(data);
    }, 1000);
}


export async function postFile(url = '',file, data = {}) {
    console.log('data',data)
    let formData = new FormData();
    formData.append("file", file);

    for (key in data) {
        formData.append(key, data[key])
    }


    
    const response = await fetch(server_url+url, { method: "POST",credentials: 'include', body: formData })

    if (response.status == 200) {
        return response.json(); // parses JSON response into native JavaScript objects
    }else {
        let val = await response.text()
        // confirmBox("Error!", val)
        confirmBox("Oops!", val)
        document.querySelectorAll('.modal-preloader').forEach(a=>a.style.display = "none");
        return Promise.reject(new Error(val))
    }
}


export function confirmBox(title, content, action = null, cancel = null,ok_text = 'Ok',cancel_text='Cancel') {
    const { $swal } = useNuxtApp()
    if (cancel){
        btn_class.customClass.confirmButton =  'btn btn-dark ms-2' 
        btn_class.showCancelButton = true
    } else {
        btn_class.customClass.confirmButton =  'btn btn-dark' 
        btn_class.showCancelButton = false
    }

    btn_class.confirmButtonText = ok_text
    btn_class.cancelButtonText = cancel_text
    

    let swal_dict = {}
    swal_dict['allowOutsideClick'] = false
    if (title == ""){
        swal_dict['icon'] = "info"
        title = "Info"
    } else if (title.toLowerCase().substring(0, 7) == "success"){
        swal_dict['icon'] = "success"
    } else if (title.toLowerCase().substring(0, 5) == "error"){
        swal_dict['icon'] = "error"
    } else if (title.toLowerCase().substring(0, 7) == "warning"){
        swal_dict['icon'] = "warning"
    } else if (title.toLowerCase().substring(0, 5) == "alert"){
        swal_dict['icon'] = "warning"
    } else if (title.toLowerCase().substring(0, 4) == "oops"){
        swal_dict['icon'] = "warning"
    }

    swal_dict['title'] = title
    if(typeof(content)!="string"){
        swal_dict['html'] = content
    }else{
        swal_dict['text'] = content
    }
    

    const swal_mixin =  $swal.mixin(btn_class);

    swal_mixin.fire(swal_dict).then((result) => {
        if (result.isConfirmed && action) {
            action()
        } else if (result.isDenied && cancel) {
            cancel()
        }
    });
}


function get_seva_element(tagname, classlist, id = null, childelement = null) {
    let element = document.createElement(tagname)
    if (id) {
        element.id = id
    }
    if (classlist) {
        class_names = classlist.split(" ")
        for (let class_name of class_names) {
            element.classList.add(class_name)
        }
    }
    if (childelement) {
        element.appendChild(childelement)
    }
    return element
}
