Roadmap / Current Limits
------------------------

* Currency symbol is hard coded. (€ for the time being);

* Dates and Prices displayed do NOT change depending of the localization of
  the user;

* JS and CSS lib are hard included. So if many apps are developped, it could
  be great to have a generic 'web_ionic' module that have all tools to avoid
  to duplicate files;

Available languages for the Mobile Application
----------------------------------------------

* English
* French

Known Issues
------------

* **Firefox Ionic Bug** : The first screen allow user to select database,
  in a multi database context. This module use ionic select component, that
  doesn't not works On Firefox Mobile.
  `See the bug on Ionic Github <https://github.com/driftyco/ionic/issues/4767>`_
  
* **Chrome Mobile limitation** : This module plays mp3 sounds.
  This feature is not available for Chrome Mobile for the time being,
  cause Chrome consider that allowing to play a sound without explicit action
  of the user raises security issues.
  `See the bug on Chromium website <https://bugs.chromium.org/p/chromium/issues/detail?id=178297>`_
