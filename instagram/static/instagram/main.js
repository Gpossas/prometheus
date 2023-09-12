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
    if ( response.ok ){
      return response.json();
    } else{
      const error = await response.json().then( message => message['error'] );
      throw new Error( `Error: ${ error }, status: ${ response.status }` );
    }
  })
  .then( data => {
    const video = htmlToElement(
      `<div class="video_preview">
          <div class="video_preview_header">
            <img src="${ data['proxy_server'] }/${ data['profile_picture'] }">
            <p>${ data['name'] }</p>
          </div>
          <img src="${ data['proxy_server'] }/${ data['video_thumbnail'] }">
        </div>`
    );
    
    videosDiv.appendChild( video );
    videosToDownload.push( [ data['name'], data['video_url'] ] ); 
  })
  .catch( error =>{
    console.log( error );
  });
}

function htmlToElement(html){
  const template = document.createElement('template');
  html = html.trim();
  template.innerHTML = html;
  return template.content.firstChild;
} 

function quitDriver( api_url ){
  fetch( api_url, {
    method: 'POST',
    headers: { 'X-CSRFToken': csrftoken },
    mode: 'same-origin', // Do not send CSRF token to another domain.  
  })
  .then( async response => {
    if ( response.ok ){
      return;
    } else{
      throw new Error( `Error quitting drive, status: ${ response.status }` );
    }
  })
  .catch( error =>{
    console.log( "couldn't quit drive", error );
  });
}



const csrftoken = getCookie( 'csrftoken' );
const videosDiv = document.querySelector( '.videos' );

const searchButton = document.querySelector( '#search_button' );
const url = document.querySelector( '#url_input' );
searchButton.addEventListener( 'click', () => getVideo( searchButton.dataset.url ) );
url.addEventListener( 'keyup', ( { key } ) => { if ( key === "Enter" ) return getVideo( searchButton.dataset.url ) } );

const videosToDownload = [];
const videosToPassToServer = document.querySelector( '#videos' );
const downloadForm = document.querySelector( '#download_form' );
downloadForm.addEventListener( 'submit', () => videosToPassToServer.value = JSON.stringify( videosToDownload ) );

const apiPathQuitDrive = document.querySelector( '#quit-driver-path' ).innerHTML;
window.addEventListener( 'beforeunload', () => quitDriver( apiPathQuitDrive ) );