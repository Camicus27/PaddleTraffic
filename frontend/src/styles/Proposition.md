It is proposed to organize css / scss in the following manner for modularity and flexible refactorability across the team.

1. Global Variables, Functions, Mixins, Placeholder Classes, and Styles stored in src/styles. 
Files for Sass will be partials, which need to be included to generate css, otherwise they will not generate css files to prevent bloated delivery

styles
|-- abstracts
    |-- _colors.scss
    |-- _fonts.scss
    |-- ...
|-- components
    |-- _buttons.scss
    |-- _forms.scss
    |-- _links.scss
    |-- ...
|-- globals
    |-- ...

Any globals will go in App.vue in the script tag as an import so that webpack can handle it.