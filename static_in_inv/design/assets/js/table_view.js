


let pageId= window.location.pathname;

let viewState = localStorage.getItem('view-' + pageId);

if (viewState == null){
    viewState = 'list';
}

if (viewState == 'grid'){
    $('#gridView').removeClass('btn-soft-secondary').addClass('btn-secondary');
    $('#listView').removeClass('btn-secondary').addClass('btn-soft-secondary');
    
}else{
    $('#listView').removeClass('btn-soft-secondary').addClass('btn-secondary');
    $('#gridView').removeClass('btn-secondary').addClass('btn-soft-secondary');
}

$('#listView').on('click', function(){
    localStorage.setItem('view-'+pageId, 'list');
    $('#listView').removeClass('btn-soft-secondary').addClass('btn-secondary');
    $('#gridView').removeClass('btn-secondary').addClass('btn-soft-secondary');

});

$('#gridView').on('click', function(){
    localStorage.setItem('view-'+pageId, 'grid');
    $('#gridView').removeClass('btn-soft-secondary').addClass('btn-secondary');
    $('#listView').removeClass('btn-secondary').addClass('btn-soft-secondary');
});



 