<template>
    <div class="container">
        <div class="d-flex justify-content-end">
            <select v-model="select_option" class="form-select form-control my-4"
                style="background-color: #fff; width: 13rem;">
                <option value="opt1">Option 1</option>
                <option value="opt2">Option 2</option>
                <option value="opt3">Option 3</option>
            </select>
        </div>
        <div class="mb-3 main">
            <div class="dropzone-container" @dragover="dragover" @dragleave="dragleave" @drop="drop">
                <input v-on:change="select_file" id="fileInput" type="file" accept="video/*" class="hidden-input">
                <label class="file-label" for="fileInput">
                    <div v-if="isDragging">Release to drop files here.</div>
                    <div v-else>Choose file to upload. <u>click here</u></div>
                </label>
                <label v-if="isfileName">{{ file_name }}</label>
            </div>
        </div>
        <div ref="progress_div" class="progress mt-3 mb-3" style="display:none;">
            <div id="progress_bar" class="progress-bar progress-bar-striped progress-bar-animated" role="progressbar"
                aria-valuenow="1" aria-valuemin="1" aria-valuemax="100" style="width: 0%">
            </div>
        </div>
        <div class="d-flex justify-content-end mb-3">
            <button v-on:click="solve_methods" type="button" class="btn btn-md btn-primary">Solve</button>
        </div>
        <div class="d-flex justify-content-between">
            <button type="button" class="btn btn-md btn-primary">Log File</button>
            <button type="button" class="btn btn-md btn-primary">Solver</button>
        </div>
    </div>
</template>
  
<script setup>
const select_option = ref('')
let isDragging = ref(false)
const file_name = ref('')
let isfileName = ref(false)
const progress_div = ref(null)

let img;
const select_file = (event) => {
    img = event.target.files[0]
    file_name.value = img.name
    isfileName.value = true
}

const dragover = (e) => {
    e.preventDefault();
    isDragging.value = true;
}
const dragleave = () => {
    isDragging.value = false;
}
function drop(e) {
    isDragging.value = false;
    e.preventDefault();
    img = e.dataTransfer.files[0];
    file_name.value = img.name
    isfileName.value = true
    console.log(img);
}

async function solve_methods() {
    console.log('img', file_name.value)
    console.log('img', img)
    if(select_option.value === ''){
        confirmBox('Alert', 'Please select option')
        return
    }
    if(!img){
        confirmBox('Alert', 'Please select video first')
        return
    }

    let loader1 = progress_div.value
    loader1.style.display = ''
    let data = await postData('/get-upload-url', { filename: img.name })
    
    console.log('data', data)
    if (!data) {
        confirmBox('Alert', "Something went wrong, Please try again later")
    }

    

    let upload_url = data['upload_url']

    const res = await fetch(upload_url, {
        method: 'PUT',
        headers: {
            'opc-multipart': true,
        }
    })

    if (res.status === 200) {
        if (res.headers.get('Content-Type') == 'application/json') {
            res.json().then(data => {
                let url = 'https://objectstorage.us-ashburn-1.oraclecloud.com' + data['accessUri']
                let upload_id = data['uploadId']

                upload_multipart_video(img, url, 'progress_bar').then(data => {
                    postData('/solve', { solver: select_option.value, filename: img.name, upload_id: upload_id }).then(data => {
                        confirmBox('Success', 'File uploaded successfully')
                        loader1.style.display = 'none'
                    })

                })
            })
        } else {
            console.log('content type not application/json')

        }

    } else {
        let val = await res.text()
        confirmBox("Oops!", val)
    }

}



//break into 30 MB chunks 
const chunkSize = 30000000;
var chunkEnd = 0
var start = 0


async function upload_multipart_video(video, url, progressbar_id) {
    var numberofChunks = Math.ceil(video.size / chunkSize);

    if (numberofChunks === 1) {
        move(50, progressbar_id)
    }

    var percentage = Math.ceil(100 / numberofChunks)

    for (let i = 0; i < numberofChunks; i++) {

        chunkEnd = Math.min(start + chunkSize, video.size);

        const chunk = video.slice(start, chunkEnd + 1);

        const res = await fetch(url + (i + 1), {
            method: 'PUT',
            body: chunk
        })

        if (res.status === 200) {
            let width = (i + 1) * percentage
            if (i === numberofChunks - 1) {
                move(100, progressbar_id)
            } else if (width < 100) {
                move(width, progressbar_id)
            }
        } else {
            let val = await res.text()
            // confirmBox("Error!", val)
            await fetch(url, {
                method: 'Post',
            })
            confirmBox("Oops!", 'Selected video is corrupted, Please try again')
            return
        }
        start = chunkEnd + 1
    }

    await fetch(url, {
        method: 'Post',
    })

}

function move(width, prgressbar_id) {
    var elem = document.getElementById(prgressbar_id);
    elem.style.width = 1 + '%';
    elem.setAttribute("aria-valuenow", width)

    if (width <= 100) {

        elem.style.width = width + '%';
        elem.innerText = width + '%';
    }
}
</script>

<style scoped>
.main {
    text-align: center;
    margin-bottom: 1.5rem;
}

.dropzone-container {
    padding: 4rem;
    background: #f7fafc;
    border: 1px solid #e2e8f0;
}

.hidden-input {
    opacity: 0;
    overflow: hidden;
    position: absolute;
    width: 1px;
    height: 1px;
}

.file-label {
    font-size: 20px;
    display: block;
    cursor: pointer;
}

.preview-container {
    display: flex;
    margin-top: 2rem;
}

.preview-card {
    display: flex;
    border: 1px solid #a2a2a2;
    padding: 5px;
    margin-left: 5px;
}

.preview-img {
    width: 50px;
    height: 50px;
    border-radius: 5px;
    border: 1px solid #a2a2a2;
    background-color: #a2a2a2;
}
</style>