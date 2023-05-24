/*
 *** 一些js公共方法
 */


function showAlert(message, type) {
  var alertBox = $('#alert-box');
  var alertMessage = $('#alert-message');
  if (type == 'error') {
    alertBox = $('#alert-box-error');
    alertMessage = $('#alert-message-error');
  } else if (type == 'warning') {
    alertBox = $('#alert-box-warning');
    alertMessage = $('#alert-message-warning');
  }
  alertMessage.text(message); // 设置弹框文字
  
  alertBox.fadeIn(); // 显示弹框
  setTimeout(function() {
    alertBox.fadeOut();
  }, 1000); // 1秒后自动关闭弹框
}

function formatDate(timestamp, format = "%Y-%m-%d %H:%M:%S") {
  const date = new Date(parseInt(timestamp) * 1000);
  const year = date.getFullYear();
  const month = ("0" + (date.getMonth() + 1)).slice(-2);
  const day = ("0" + date.getDate()).slice(-2);
  const hour = ("0" + date.getHours()).slice(-2);
  const minute = ("0" + date.getMinutes()).slice(-2);
  const second = ("0" + date.getSeconds()).slice(-2);
  return format
    .replace("%Y", year)
    .replace("%m", month)
    .replace("%d", day)
    .replace("%H", hour)
    .replace("%M", minute)
    .replace("%S", second);
}

function logoutEventBind() {
  let logout = document.getElementById('logout');
  logout.addEventListener('click', () => {
    fetch('/logout')
      .then(function(response) {
        return response.json();
      })
      .then(function(response){
        showAlert(response.msg, response.status);
        setTimeout(() => {
          window.location.href =  '/login';
        }, 1000);
      })
  });
}

/* function downloadPDF(ele) {
  var element = ele; // 这个dom元素是要导出pdf的div容器
  console.log(element);
  if (!element) return;

  const resp = domtoimage.toPng(element);
  let contentWidth = element.clientWidth;
  let contentHeight = element.clientHeight;

  let pageHeight = (contentWidth / 592.28) * 841.89;
  //未生成pdf的html页面高度
  let leftHeight = contentHeight;
  //页面偏移
  let position = 0;
  //a4纸的尺寸[595.28,841.89]，html页面生成的canvas在pdf中图片的宽高
  let imgWidth = 595.28;
  let imgHeight = (592.28 / contentWidth) * contentHeight;
  let pdf = new jsPDF("", "pt", "a4");

  //有两个高度需要区分，一个是html页面的实际高度，和生成pdf的页面高度(841.89)
  //当内容未超过pdf一页显示的范围，无需分页
  if (leftHeight < pageHeight) {
    pdf.addImage(resp, "JPEG", 0, 0, imgWidth, imgHeight);
  } else {
    while (leftHeight > 0) {
      pdf.addImage(resp, "JPEG", 0, position, imgWidth, imgHeight);
      leftHeight -= pageHeight;
      position -= 841.89;
      //避免添加空白页
      if (leftHeight > 0) {
        pdf.addPage();
      }
    }
  }
  pdf.save('content.pdf');
}; */

function downloadPDF(ele) {
  var element = ele;
  console.log(element);
  if (!element) return;

  domtoimage.toPng(element).then(function (resp) {
    let contentWidth = element.clientWidth;
    let contentHeight = element.clientHeight;

    let pageHeight = (contentWidth / 592.28) * 841.89;
    let leftHeight = contentHeight;
    let position = 0;
    let imgWidth = 595.28;
    let imgHeight = (592.28 / contentWidth) * contentHeight;
    let pdf = new jsPDF("", "pt", "a4");

    if (leftHeight < pageHeight) {
      pdf.addImage(resp, "PNG", 0, 0, imgWidth, imgHeight);
    } else {
      while (leftHeight > 0) {
        pdf.addImage(resp, "PNG", 0, position, imgWidth, imgHeight);
        leftHeight -= pageHeight;
        position -= 841.89;
        if (leftHeight > 0) {
          pdf.addPage();
        }
      }
    }

    pdf.save('content.pdf');
  }).catch(function (error) {
    console.error('dom-to-image 转换成图片出错：', error);
  });
};

function downloadPDFOnePage(ele) {
  var element = ele;
  console.log(element);
  if (!element) return;

  domtoimage.toPng(element).then(function (resp) {
    let contentWidth = element.clientWidth;
    let contentHeight = element.clientHeight;

    let imgWidth = 595.28;
    let pageHeight = (contentHeight / contentWidth) * imgWidth;
    let pdf = new jsPDF("", "pt", "a4");

    pdf.addImage(resp, "PNG", 0, 0, imgWidth, pageHeight);

    pdf.save('content.pdf');
  }).catch(function (error) {
    console.error('dom-to-image 转换成图片出错：', error);
  });
};
