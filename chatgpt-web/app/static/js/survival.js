// 假设您有一个ID为'survival-form'的表单和一个ID为'prediction-result'的元素用于显示结果
document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('surival-form');

    form.onsubmit = function(e) {
        e.preventDefault(); // 阻止表单的默认提交行为

        // 使用FormData收集表单数据
        var formData = new FormData(form);

        // 发送POST请求到Flask后端
        fetch('/survival', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if(data.error) {
                alert(data.error); // 或者在页面上显示错误信息
            } else {
                // 将预测结果显示到页面上
                document.getElementById('prediction-result').textContent = 'Predicted survival rate: ' + data.prediction;
            }
        })
        .catch(error => console.error('Error:', error));
    };
});
