const CookiesHandler = function (cookieName, dsfr) {
    let currentAuthorizations = {};
    let cookiesEvents = [];
    let thirdCookiesNames = [];
    let modal = {};
    let banner = {};
    const self = this;

    function removeAll() {
        const authorizedList = [];
        setAuthorizations(authorizedList);
        closeBanner();
    }

    function acceptAll() {
        const authorizedList = thirdCookiesNames;
        setAuthorizations(authorizedList);
        closeBanner();
    }

    function confirmChoices() {
        const authorizedList = thirdCookiesNames.filter(thirdCookieName =>
            document.querySelector('input[name=' + thirdCookieName + ']:checked').value === '1'
        );
        setAuthorizations(authorizedList);
        closeModal();
        closeBanner();
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
        modal = params.modal;
        banner = params.banner;
        thirdCookiesNames = Object.keys(params.events);
        currentAuthorizations = getAuthorizations();
        initEvents(params);
        initCheckboxes(currentAuthorizations);
        dispatchCookies(currentAuthorizations);
    }

    function dispatchCookies(authorizedList) {
        cookiesEvents.forEach(event => {
            if (authorizedList.includes(event.type)) {
                self.dispatchEvent(event);
            }
        });
    }

    function setAuthorizations(authorizedList) {
        localStorage.setItem('cnrAuthorisedCookies', authorizedList);
        dispatchCookies(authorizedList);
    }

    function closeBanner() {
        banner.classList.remove('fr-unhidden');
        banner.classList.add('fr-hidden');
    }

    function openBanner() {
        banner.classList.remove('fr-hidden');
        banner.classList.add('fr-unhidden');
    }

    function closeModal() {
        dsfr(modal).modal.conceal();
    }

    function initCheckboxes(authorizedList) {
        thirdCookiesNames.forEach(thirdCookieName =>
            document.querySelectorAll('input[name=' + thirdCookieName + ']').forEach(radio =>
                radio.checked = (radio.value === '1' && authorizedList.includes(thirdCookieName)) || (!authorizedList.includes(thirdCookieName))
            )
        );
    }

    function getAuthorizations() {
        console.log(localStorage.getItem('cnrAuthorisedCookies'));
        if (localStorage.getItem('cnrAuthorisedCookies') === null) {
            openBanner();
            return [];
        } else {
            return localStorage.getItem('cnrAuthorisedCookies').split(',');
        }
    }

    return {
        init
    };
};