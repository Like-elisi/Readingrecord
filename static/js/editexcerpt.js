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

    $("#submit").click(function(event){
        // 阻止按钮的默认行为
        event.preventDefault();

        let title = $("input[name='title']").val();
        let page_number = $("input[name='page_number']").val();
        let content = $("input[name='content']").val();
        let feeling = $("input[name='feeling']").val();
        let csrfmiddlewaretoken = $("input[name='csrfmiddlewaretoken']").val();
        $.ajax('book/edit_excerpt', {
            method: 'POST',
            data: {title, page_number, content, feeling,csrfmiddlewaretoken},
            success: function(result){
                if(result['code'] == 200){
                    // 获取博客id
                    let book_id = result['data']['book_id']
                    // 跳转到博客详情页面
                    window.location = 'book/edit_excerpt' + book_id
                }else{
                    alert(result['message']);
                }
            }
        })
    });
}