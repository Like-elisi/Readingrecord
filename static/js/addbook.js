window.onload = function () {
    const {createEditor, createToolbar} = window.wangEditor

    const editorConfig = {
        placeholder: 'Type here...',
        onChange(editor) {
            const html = editor.getHtml()
            console.log('editor content', html)
            // 也可以同步到 <textarea>
        }
    }

    const editor = createEditor({
        selector: '#editor-container',
        html: '<p><br></p>',
        config: editorConfig,
        mode: 'default', // or 'simple'
    })

    const toolbarConfig = {}

    const toolbar = createToolbar({
        editor,
        selector: '#toolbar-container',
        config: toolbarConfig,
        mode: 'default', // or 'simple'
    })

    $("#save").click(function(event){
        // 阻止按钮的默认行为
        event.preventDefault();

        let title = $("input[name='title']").val();
        let statues = $("#statues-select").val();
        let author = $("input[name='author']").val();
        let language = $("input[name='language']").val();
        let publishyear = $("input[name='publishyear']").val();
        let type = $("input[name='type']").val();
        editor.config.uploadImgShowBase64 = true;
        let cover = editor.getHtml();
        let csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();
        $.ajax('/addbook', {
            method: 'POST',
            data: {title, author, statues,language,publishyear,type,cover,csrfmiddlewaretoken},
            success: function(result){
                if(result['code'] == 200){
                    // 获取博客id
                    let book_id = result['data']['book_id']
                    // 跳转到博客详情页面
                    window.location = 'book/detail/' + book_id
                }else{
                    alert(result['message']);
                }
            }
        })
    });
}