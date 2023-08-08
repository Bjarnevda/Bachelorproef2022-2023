declare global {
  interface JQuery {
    owlCarousel(options?: any): JQuery;
  }

  interface JQuery<TElement extends HTMLElement> {
    modal(action: string): void;
  }
}