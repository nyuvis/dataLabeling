function renderTable() {
    $(document).ready(function() {
        $('#docs_table').empty();
        let head = '<thead><tr><th scope="col">ID</th><th scope="col">Content</th><th scope="col">Label</th></tr></thead>'
        $("#docs_table").append(head);
        $("#docs_table").append('<tbody id="docs_table_content"></tbody>');
        let key_list = []
        for (let i=0; i < 20; i++){
            let id = i
            let content = '<tr><td>' + id + '</td><td>' + data_dict[id]['doc'] + '</td><td>' + data_dict[id]['ori_cat'] + '</td></tr>'
            $("#docs_table_content").append(content);
        }

        // for (let id in data_dict) {
        //     console.log(id)
        //     let content = '<tr><td>' + id + '</td><td>' + data_dict[id]['doc'] + '</td><td>' + data_dict[id]['ori_cat'] + '</td></tr>'
        //     $("#docs_table_content").append(content);
        // }
    });
}