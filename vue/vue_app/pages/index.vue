<template>
    <div class="container">
        <select v-model="select_option" class="form-select form-control my-4" style="background-color: #fff;">
            <option value="opt1">Option 1</option>
            <option value="opt2">Option 2</option>
            <option value="opt3">Option 3</option>
        </select>
        <div class="mb-3">
            <label class="form-label" for="specialAd_img_inp">Upload Image</label>
            <input v-on:change="select_file" type="file" accept="video/*" class="form-control">
        </div>
        <button v-on:click="solve_methods" type="button" class="btn btn-md btn-primary">Solve</button>
    </div>
</template>
  
<script setup>
    const select_option = ref('')

    let img;
    const select_file = (event) =>{
        img = event.target.files[0]
    }

    async function solve_methods(){
        console.log('img',img.name)
        let data = await postData('/get-upload-url',{filename:img.name})
        console.log('data',data)
        if (!data){        
            confirmBox('Alert',"Something went wrong, Please try again later")
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
                        postData('/solve',{solver:select_option.value,filename:img.name,upload_id:upload_id}).then(data=>{
                            console.log('Success','File uploaded successfully')
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

        // if (numberofChunks === 1) {
        //     move(50, progressbar_id)
        // }

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
                // if (i === numberofChunks - 1) {
                //     move(100, progressbar_id)
                // } else if (width < 100) {
                //     move(width, progressbar_id)
                // }
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