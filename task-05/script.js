class Header extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
      <nav>            
       <div class="navbar">
                <a href="index.html"><img class="navbar-logo" src="assets/navbar/logo.png"></a>
                <div class="navbar-social">
                    <a href="https://open.spotify.com/artist/53XhwfbYqKCa1cC15pYq2q"><img class="navbar-social-items" src="assets/navbar/Spotify.svg"></a>
                    <a href="https://www.youtube.com/channel/UCT9zcQNlyht7fRlcjmflRSA"><img class="navbar-social-items" src="assets/navbar/youtube.svg"></a>
                    <a href="https://twitter.com/Imaginedragons"><img class="navbar-social-items" src="assets/navbar/twitter.svg"></a>
                </div>
            </div>       
      </nav>
    `;
  }
}

customElements.define('nav-bar', Header);