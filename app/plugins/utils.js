import Vue from "vue";

Vue.prototype.$idealTextColor = bgColor => {
  const [r, g, b] = parseColor(bgColor);

  const yiq = (r * 299 + g * 587 + b * 114) / 1000;

  return yiq >= 128 ? "4d4d4d" : "f2f2f2";
};

Vue.prototype.$brighterColor = (color, percent) => {
  const [r, g, b] = parseColor(color);

  return (
    (0 | ((1 << 8) + r + ((256 - r) * percent) / 100)).toString(16).substr(1) +
    (0 | ((1 << 8) + g + ((256 - g) * percent) / 100)).toString(16).substr(1) +
    (0 | ((1 << 8) + b + ((256 - b) * percent) / 100)).toString(16).substr(1)
  );
};

function parseColor(color) {
  const r = parseInt(color.substr(0, 2), 16);
  const g = parseInt(color.substr(2, 2), 16);
  const b = parseInt(color.substr(4, 2), 16);

  return [r, g, b];
}
