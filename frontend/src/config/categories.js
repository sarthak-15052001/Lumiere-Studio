export const CATEGORIES = [
  {
    value: "Fashion",
    label: "Fashion & Apparel",
    subcategories: [
      { value: "Women", label: "Women's Fashion", defaultRegion: "Indian" },
      { value: "Men", label: "Men's Fashion", defaultRegion: "Indian" },
      { value: "Kids", label: "Kids Fashion", defaultRegion: "Indian" },
    ],
  },
  {
    value: "Accessories",
    label: "Accessories",
    subcategories: [
      { value: "Bags & Purses", label: "Bags & Purses", defaultRegion: "Indian" },
      { value: "Jewelry", label: "Jewellery", defaultRegion: "None" },
      { value: "Watches", label: "Watches", defaultRegion: "Indian" },
    ],
  },
  {
    value: "E-commerce",
    label: "E-commerce",
    subcategories: [
      { value: "Home Decor", label: "Home Decor", defaultRegion: "None" },
      { value: "Electronics", label: "Electronics", defaultRegion: "None" },
      { value: "Other", label: "Other", defaultRegion: "None" },
    ],
  },
];

export function getCategory(categoryValue) {
  return CATEGORIES.find((c) => c.value === categoryValue) || CATEGORIES[0];
}

export function getSubcategories(categoryValue) {
  return getCategory(categoryValue).subcategories;
}

export function getDefaultRegionFor(categoryValue, subcategoryValue) {
  const sub = getSubcategories(categoryValue).find((s) => s.value === subcategoryValue);
  return sub ? sub.defaultRegion : "Indian";
}