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
      url.value = '';
      throw new Error( `Error: couldn't find video, status: ${ response.status }` );
    }
  })
  .then( data => {
    console.log(data)
    //TODO: create a more complex element, a preview of the page using name and profile_picture
    const video = document.createElement('p');
    video.textContent = data['name'];
    videosDiv.appendChild( video );
  })
  .catch( error =>{
    console.log( "couldn't find video" );
  });
}

const csrftoken = getCookie( 'csrftoken' );
const searchButton = document.querySelector( '#search_button' );
const url = document.querySelector( '#url_input' );
const videosDiv = document.querySelector( '.videos' );

searchButton.addEventListener( 'click', () => getVideo( searchButton.dataset.url ) );