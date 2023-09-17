function getCookie(name) {
  const cookies = document.cookie.split(';');
  for (const cookie of cookies) {
    const [cookieName, cookieValue] = cookie.split('=');
    if (decodeURIComponent(cookieName.trim()) === name) {
      console.log(cookie)
      return decodeURIComponent(cookieValue);
    }
  }
  return null;
}

function setCookie(name, value, hours) {
  const expires = new Date();
  expires.setTime(expires.getTime() + hours * 60 * 60 * 1000);
  const cookieValue = encodeURIComponent(name) + '=' + encodeURIComponent(value) + ';expires=' + expires.toUTCString() + ';path=/';
  document.cookie = cookieValue;
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
    
    url.value = '';
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

const apptoken = setCookie('appRun', "userUUID", 7);
const csrftoken = getCookie( 'appRun' );
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