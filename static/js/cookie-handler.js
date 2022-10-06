const CookiesHandler = function (cookieName) {
    let currentAuthorizations = {};
    let cookiesEvents = [];
    let thirdCookiesNames = [];
    const self = this;

    function removeAll() {
        const authorizedList = [];
        setAuthorizations(authorizedList);
        console.log('remove all');
    }

    function acceptAll() {
        const authorizedList = thirdCookiesNames;
        setAuthorizations(authorizedList);
        console.log('accept all');
    }

    function confirmChoices() {
        const authorizedList = [];
        setAuthorizations(authorizedList);
    }

    function initEvents(params) {
        params.acceptAllButton.addEventListener('click', (e) => {
            acceptAll();
        });

        params.acceptNoneButton.addEventListener('click', (e) => {
            removeAll();
        });

        params.confirmChoicesButton.addEventListener('click', (e) => {
            confirmChoices();
        });

        cookiesEvents = thirdCookiesNames.map(thirdCookieName => {
            self.addEventListener(thirdCookieName, params.events[thirdCookieName]);
            return new Event(thirdCookieName);
        });
    }

    function init(params) {
        thirdCookiesNames = Object.keys(params.events);
        currentAuthorizations = getAuthorizations();
        initEvents(params);
        dispatchCookies(currentAuthorizations);
    }

    function dispatchCookies(authorizedList) {
        cookiesEvents.map(event => {
            if (authorizedList.includes(event.type)) {
                self.dispatchEvent(event);
            }
        });
    }

    function setAuthorizations(authorizedList) {
        localStorage.setItem('cnrAuthorisedCookies', authorizedList);
        dispatchCookies(authorizedList);
    }

    function getAuthorizations() {
        return localStorage.getItem('cnrAuthorisedCookies').split(',') || [];
    }

    return {
        init
    };
};