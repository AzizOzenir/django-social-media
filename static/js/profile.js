const toggleButton1 = document.getElementById('toggleButton1');
const myDiv1 = document.getElementById('scroll-div1');
const header = document.getElementById("header")
const toggleButton2 = document.getElementById('toggleButton2');
const myDiv2 = document.getElementById('scroll-div2');



toggleButton1.addEventListener('click', function (event) {

    if (myDiv1.style.display === 'none') {
        myDiv1.style.display = 'block';

    } else {
        myDiv1.style.display = 'none';


    }
});



toggleButton2.addEventListener('click', function () {
    if (myDiv2.style.display === 'none') {
        myDiv2.style.display = 'block';

    } else {
        myDiv2.style.display = 'none';


    }
});



document.getElementById('post-button').addEventListener('click', function () {
    const content = document.getElementById('content');
    content.scrollIntoView({ behavior: 'smooth' });
});
