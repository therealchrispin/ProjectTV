$(document).ready(function () {
    var name;
    var omdbApiUrl;
    var serienUrl;
    var seasonNr;
    var episodeNr;
    //   var episodeCount;
    var liste;
    var container = document.getElementById('container');


var video = document.getElementById('video');
var test = -20;

$('#video-container').hide();
$('.progress').hide();

    
function progressBarAnimate(){
    $(".progress-bar").animate({
        width: "100%"
    }, 13000);
        $(".progress-bar").animate({
        width: "0%"
    },0);
}    
    

$('#play-icon').click(function() {
        var video = document.getElementById('video');
        var pauseicon = $('#pause-icon').val();
        if(video.paused){
            video.play();
            $(this).text('\u25AE'+'\u25AE');
        }else{
            video.pause();
            $(this).text('\u25b6');
        }
    });

$('#next-icon').click(function(){
    episodeNr +=1;
    getEpisode();
});

$('#last-icon').click(function(){
    episodeNr-=1;
    getEpisode();
});

$('#volume').change(function(){
    var video = document.getElementById('video');
    video.volume = document.getElementById('volume').value;
});

$('#volume-icon').click(function(){
    document.getElementById('volume').value = 0;
    document.getElementById('video').volume = 0;
});

$('#seek-bar').change(function(){
    var video = document.getElementById('video');
    var time = video.duration * (document.getElementById('seek-bar').value/100);

    video.currentTime = time;
});

$('#video').bind('timeupdate',function(){
    var video = document.getElementById('video');
    var value = (100/video.duration) * video.currentTime;

    document.getElementById('seek-bar').value = value;
});

$('#fullscreen-icon').click(function(){
    var video = document.getElementById('video-container');
    if (video.requestFullscreen) {
        video.requestFullscreen();
      } else if (video.mozRequestFullScreen) {
        video.mozRequestFullScreen(); // Firefox
      } else if (video.webkitRequestFullscreen) {
        video.webkitRequestFullscreen(); // Chrome and Safari
      }
});

function automaticPlay(){
    if($('#detailView').not(":visible")){
        $('#video-container').show();    
    }
    $('.progress').hide();
    video.load();
    video.play();
    video.addEventListener("timeupdate",function() {
        time = parseInt(video.currentTime);
        dura = test + video.duration;
        if(time > dura){
            episodeNr +=1;
            test += 20;
            getEpisode();
        }
        var currentMin = parseInt(time/60);
        var currentSec = ((time/60 - currentMin)*60).toFixed();
        var durationMin = parseInt(video.duration/60);
        var durationSec = ((video.duration/60 - durationMin)*60).toFixed();
        $('#clock').text(currentMin + ":" + currentSec +'/'+ durationMin+':'+durationSec);
        
    });
}

function getEpisode() {
    $.getJSON('http://129.187.39.211:5000/get_episodes',
    {url:serienUrl,
    season:seasonNr,
    episode:episodeNr},function(data){
        $('#source').attr('src',data.ergebnis);
        if (test == 0){
            test -= 20;
        }
        automaticPlay();
    });
    }

function getSerie(){
        $.getJSON('http://129.187.39.211:5000/get_serie_url',
        {serie:name},
        function(data){
            omdbApiUrl = data.ergebnis[0];
            serienUrl = data.ergebnis[1];
            getEpisode();
        });
}

$('#button').click(function(){
    name = document.getElementById('serienInput').value;
    var title ="";
    var poster ="";
    $.getJSON('http://129.187.39.211:5000/get_serie_url',
        {serie:name},
        function(data){
            omdbApiUrl = data.ergebnis[0];
            serienUrl = data.ergebnis[1];
            $.getJSON('http://www.omdbapi.com/?t='+data.ergebnis[0]+'&y=&plot=short&r=json',
                     function(data){
                        title = data.Title;
                        $.getJSON('http://129.187.39.211:5000/get_poster',
                                 {Title:data.Title,
                                 Poster:data.Poster},
                                 function(data){
                                     openDetailView(data.ergebnis[0],data.ergebnis[1]);
                });
            });
        });
});

function fillContainer(){
    $.getJSON('http://129.187.39.211:5000/animated',
            function(data){
                pupulate(data.ergebnis,'#container');
    });
}

function fillComdedyContainer(){
    $.getJSON('http://129.187.39.211:5000/comedy',
            function(data){
                pupulate(data.ergebnis,'#comedyContainer');
    });
    
}
    
function fullDramaContainer(){
    $.getJSON('http://129.187.39.211:5000/drama',
            function(data){
                pupulate(data.ergebnis,'#dramaContainer');
    });
}

        
function pupulate(imgListe,id){
    var img;
    liste = imgListe;
    var index = 0;
    for (var i = 0; i < imgListe.length; i++){
        var div = '<span class="ImgSpan">';
        img = jQuery(
                    div
                    +'<div class="item">'
                    +'<img class="fotos" '
                    + 'src="'+imgListe[index][1].replace('http://127.0.0.1:5000/static/images/','http://129.187.39.211:5000/static/images/') +'" ' 
                    + 'title="'+imgListe[index][0]+'" '
                    +'>'
                    +'</div>'
                    +'</span>');
        jQuery(id).append(img);
        index++
    }
}

fillContainer();
fillComdedyContainer();
fullDramaContainer();


$('#detailView').hide();

$('.imgContainer').on('click','img',function() {
    var title = $(this).attr('title');
    var poster = $(this).attr('src');
    openDetailView(title,poster);
});

function openDetailView(title,poster){
    if($('#detailView').is(":visible")){
        $('li').remove('#seasonli');
        $('div').remove('.seasonDiv');
    }
    
    $('#detailViewHead').text(title);
    $('#detailViewImg').attr('src',poster);
    $('#detailView').show();
    var button;
    
    $.getJSON('http://www.omdbapi.com/?t='+title.replace(' ','+')+'&y=&plot=short&r=json',
             function(data){
                var totals = parseInt(data.totalSeasons)+1
                for(var i = 1;i<totals;i++){
                    button = jQuery(fillSeasons(i));
                    fillEpisodes(data.Title,i);
                    jQuery('#seasongroup').append(button);
    }
    });
    name = title;    
}
    
$('.imgContainer').on('click','.scroll',function(){
        var scrollposition = $(this).parent().find('div').scrollTop();
      if (scrollposition + $(this).parent().find('div').innerHeight() >=  $(this).parent().find('div').scrollHeight) {
          $(this).parent().find('div').scrollTop(0);
      }else{
          $(this).parent().find('div').scrollTop(scrollposition + 240);
      }
});
    
    
$('.imgContainer').on('click','.scrollDown',function(){
    var scrollposition =  $(this).parent().find('div').scrollTop();
     $(this).parent().find('div').scrollTop(scrollposition - 240);
});
    
function fillSeasons(seasonNumber){
    
    var dropDown = '<li id="seasonli"><a href="#staffel'+seasonNumber+'">'
    if (seasonNumber == 1){
       dropDown = '<li class="active" id="seasonli"><a href="#staffel'+seasonNumber+'">' 
    }
                    
    dropDown += 'Season ' + seasonNumber
            + '</a></li>'
    
    return dropDown;
}

function fillEpisodes(title,seasonNumber){
    var Div;
    $.getJSON('http://www.omdbapi.com/?t='+title.replace(' ','+')+'&season='+seasonNumber,
             function(data){
                var episodes = data.Episodes;
                var seasonDiv = '<div id="staffel'+data.Season+'" class="seasonDiv">'
                                +'<h1>'+data.Title+ ' season '+data.Season+'</h1>'
                                +'<div class="list-group">';
                var seasonDivEnd = '</div></div>';
                var episode = "";
                for(var i = 0;i<data.Episodes.length;i++){
                    episode += '<a href="#" class="list-group-item" '
                        +'id="'+data.Season+'" '
                        +'title="'+data.Episodes[i].Episode+'"'
                        +'>'+data.Episodes[i].Episode + ' ' + data.Episodes[i].Title+'</a>';
                }
    
                var div = jQuery(seasonDiv + episode + seasonDivEnd);
                jQuery('#episodesContainer').append(div);
        }); 
}
    
    
$('#episodesContainer').on('click','a',function(){
    episodeNr = parseInt($(this).attr('title'));
    seasonNr = parseInt($(this).attr('id'));
    $('#video-container').hide();
    if(video.paused){
        }else{
            video.pause();
        }
    
    $('.progress').show();
    progressBarAnimate();

    getSerie();
})

             
              
$('.scroll').click(function(){
    var scrollposition = $(this).parent().find('div').scrollTop();
      if (scrollposition + $(this).parent().find('div').innerHeight() >= $(this).parent().find('div').scrollHeight) {
          $(this).parent().find('div').scrollTop(0);
      }else{
          $(this).parent().find('div').scrollTop(scrollposition + 240);
      }
     
});
    
$('.scrollDown').click(function(){
    var scrollposition = $(this).parent().find('div').scrollTop();
    $(this).parent().find('div').scrollTop(scrollposition - 240);
});    


    
    
    
    
    
});