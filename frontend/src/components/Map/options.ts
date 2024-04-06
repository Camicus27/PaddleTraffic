import {
    type DrawType,
    type TypeNumber,
    type Mode,
    type ErrorCorrectionLevel,
    type DotType,
    type CornerSquareType,
    type CornerDotType
  } from 'qr-code-styling';

const bg_color = '#71864f'
const size = 290

const options = {
    width: size,
    height: size,
    type: 'svg' as DrawType,
    data: 'http://qr-code-styling.com',
    image: '/logoForQR_dark.png',
    margin: 5,
    qrOptions: {
      typeNumber: 0 as TypeNumber,
      mode: 'Byte' as Mode,
      errorCorrectionLevel: 'Q' as ErrorCorrectionLevel
    },
    imageOptions: {
      hideBackgroundDots: true,
      imageSize: 0.8,
      margin: 6,
      crossOrigin: 'anonymous',
    },
    dotsOptions: {
      color: bg_color,
      type: 'dots' as DotType
    },
    backgroundOptions: {
      color: '#ffffff',
    },
    cornersSquareOptions: {
      color: bg_color,
      type: 'extra-rounded' as CornerSquareType,
    },
    cornersDotOptions: {
      color: bg_color,
      type: 'dot' as CornerDotType,
    }
  };

  export default options