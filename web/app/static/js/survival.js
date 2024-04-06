// 监听 DOMContentLoaded 事件以确保页面已加载
document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('survival-form');
    var resultDiv = document.querySelector('.result'); // 获取结果 div

    form.onsubmit = function(e) {
        e.preventDefault(); // 阻止表单的默认提交行为

        var formData = new FormData(form);
        fetch("{{ url_for('main.survival') }}", {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if(data.prediction) {
                document.getElementById('prediction-result').textContent = 'Predicted survival rate: ' + data.prediction + ' %';
                resultDiv.style.display = "block"; // 显示结果 div
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };
});