function getCookie( name ) {
  let cookieValue = null;
  if ( document.cookie && document.cookie !== '' ) {
    const cookies = document.cookie.split( ';' );
    for ( let i = 0; i < cookies.length; i++ ) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if ( cookie.substring( 0, name.length + 1 ) === ( name + '=' ) ) {
        cookieValue = decodeURIComponent( cookie.substring( name.length + 1 ) );
        break;
      }
    }
  }
  return cookieValue;
}

function getVideo( api_url ){
  fetch( api_url, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrftoken },
    mode: 'same-origin', // Do not send CSRF token to another domain.  
    body: JSON.stringify( { url: url.value } ),
  })
  .then( async response => {
    url.value = '';
    if ( response.ok ){
      return response.json();
    } else{
      throw new Error( `Error: couldn't find video, status: ${ response.status }` );
    }
  })
  .then( data => {
    console.log(data)
    //TODO: create a more complex element, a preview of the page using name and profile_picture
    //TODO: solve blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.

    const video = document.createElement('p');
    video.textContent = data['name'];    
    videosDiv.appendChild( video );

    videosToDownload.push( [ data['name'], data['video_url'] ] )
  })
  .catch( error =>{
    console.log( "couldn't find video" );
  });
}

function downloadVideos( api_url ){
  fetch( api_url, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrftoken },
    mode: 'same-origin', // Do not send CSRF token to another domain.  
    body: JSON.stringify( videosToDownload ),
  })
  .then( async response => {
    if ( response.ok ){
      return response.json();
    } else{
      throw new Error( `Error downloading videos, status: ${ response.status }` );
    }
  })
  .then( data => {
    console.log(data)
  })
  .catch( error =>{
    console.log( "couldn't download video" );
  });
}

const videosToDownload = [];
const downloadButton = document.querySelector( '#download_button' )

const csrftoken = getCookie( 'csrftoken' );
const searchButton = document.querySelector( '#search_button' );
const url = document.querySelector( '#url_input' );
const videosDiv = document.querySelector( '.videos' );

searchButton.addEventListener( 'click', () => getVideo( searchButton.dataset.url ) );
downloadButton.addEventListener( 'click', () => downloadVideos( downloadButton.dataset.url ) );