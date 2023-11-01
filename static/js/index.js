function likeHandler() {

const likeLink = document.getElementById('likeLink');

likeLink.href = `/like?post_id=${post.id}&scroll=${window.scrollY}`;
console.log(likeLink.href)
window.location.href = likeLink.href;
}
