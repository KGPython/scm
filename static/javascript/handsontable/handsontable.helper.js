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