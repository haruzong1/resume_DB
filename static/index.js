function onboarding() {
    var writer = $('#inputGroupSelect01 option:selected').text()

    $.ajax({
        type: "POST",
        url: "/info",
        data: {'writer_give': writer},
        success: function (response) { // 성공하면
            if (response["result"] == "success") {
                alert(response["msg"]);
                window.location.reload();
            } else {
                alert('서버오류입니다.')
            }
        }
    })
}
function showDB() {
window.open('showDB.html')
}

// apply : if 모든 정보값 있음 -> 데이터 베이스에 등록
//            특정 정보값 누락 -> 해당 데이터 기록 alert
//질문 : 스파르타에서는
// function apply() {
//     let DBwriter = $('inputGroupSelect01').val();
//     let DBkind = $('inputGroupSelect02').val();
//     let name = $('#mktName').val();
//     let birth = $('mktBirth').val();
//     let email = $('#mktEmail').val();
//     let phone = $('#mktPhone').val();
//     let salary = $('#mktSalary').val();
//     let career = $('#mktCareer').val();
//     let universe = $('#mktUn').val();
//     let resume = $('#inputGroupFile01').val();
//     let portfolio = $('#inputGroupFile02').val();
//
//     let rightEmail = /^[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_.]?[0-9a-zA-Z])*.[a-zA-Z]{2,3}$/i;
//     if (name == '') {
//         alert('이름을 적어주세요')
//         $('#mktName').focus()
//     } else if (email == '') {
//         alert("이메일을 적어주세요.")
//         $('#mktEmail').focus()
//     } else if (rightEmail.test(email) == false) {
//         alert("잘못된 이메일 형식입니다.")
//         $('#mktEmail').focus()
//         return
//     } else if (phone == '') {
//         alert("연락처를 적어주세요")
//         $('#mktPhone').focus()
//     } else if (career == '') {
//         alert("연차를 적어주세요")
//         $('#mktCareer').focus()
//     } else if (career == '') {
//         alert("연차를 적어주세요")
//         $('#mktCareer').focus()
//     } else if (salary == '') {
//         alert('연봉 적어주세요,')
//         $('#mktSalary').focus()
//     } else if (resume == '') {
//         alert('이력서 파일을 제출해주세요.')
//         $('#inputGroupFile01').focus()
//     } else {
//         alert('DB등록완료')
//     }
// }
