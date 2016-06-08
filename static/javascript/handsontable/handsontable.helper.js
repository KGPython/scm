/**
 * Created by liubf on 2016-5-12.
 */
function headerRenderer(instance, td, row, col, prop, value, cellProperties) {
  Handsontable.renderers.TextRenderer.apply(this, arguments);
  td.style.fontWeight = 'bold';
  td.style.color = '#000';
  td.style.background = '#D8D4BB';
}
function headerTextRenderer(instance, td, row, col, prop, value, cellProperties) {
  Handsontable.renderers.TextRenderer.apply(this, arguments);
  td.style.fontWeight = 'bold';
  td.style.color = '#BD0000';
  td.style.background = '#D8D4BB';
}
function rowRenderer1(instance, td, row, col, prop, value, cellProperties) {
  Handsontable.renderers.TextRenderer.apply(this, arguments);
  td.style.color = '#000';
  td.style.background = '#D8E4BC';
}

function rowRenderer2(instance, td, row, col, prop, value, cellProperties) {
  Handsontable.renderers.TextRenderer.apply(this, arguments);
  td.style.color = '#000';
  td.style.background = '#92D050';
}

function sumRenderer(instance, td, row, col, prop, value, cellProperties) {
  Handsontable.renderers.TextRenderer.apply(this, arguments);
  td.style.fontWeight = 'bold';
  td.style.color = '#000';
  td.style.background = '#FFFF99';
}
function sumRenderer_middle(instance, td, row, col, prop, value, cellProperties) {
  Handsontable.renderers.TextRenderer.apply(this, arguments);
  td.style.fontWeight = 'bold';
  td.style.color = '#000';
  td.style.background = '#FFFF00';
}

function sumRenderer_deep(instance, td, row, col, prop, value, cellProperties) {
  Handsontable.renderers.TextRenderer.apply(this, arguments);
  td.style.fontWeight = 'bold';
  td.style.color = '#000';
  td.style.background = '#FFC000';
}

//设置cells样式 ，手动将该函数注册到Handsontable ，注册方式：Handsontable.renderers.registerRenderer('negativeValueRenderer', negativeValueRenderer);
function negativeValueRenderer(instance, td, row, col, prop, value, cellProperties) {
    Handsontable.renderers.TextRenderer.apply(this, arguments);
    // if row contains negative number
    if (parseInt(value) < 100) {
      // add class "negative"
      td.style.fontWeight = 'bold';
      td.style.color = '#BD0000';
      td.style.background = '#D8D4BB';
    }

    if (!value || value === '') {
      td.style.background = '#EEE';
    }
    else {
      if (value === 'Nissan') {
        td.style.fontStyle = 'italic';
      }
      td.style.background = '';
    }
  }
