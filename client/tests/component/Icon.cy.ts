import Icon from '@/components/common/Icon.vue'

describe('Icon', () => {
  it('renders a use element referencing the icon sprite', () => {
    cy.mount(Icon, { props: { name: 'logo' } })
    cy.get('svg.sa-icon use').should('have.attr', 'href', '#icon-logo')
  })

  it('defaults to size m', () => {
    cy.mount(Icon, { props: { name: 'logo' } })
    cy.get('svg.sa-icon').should('have.class', 'sa-icon--m')
  })

  it('applies the requested size class', () => {
    cy.mount(Icon, { props: { name: 'logo', size: 'xl' } })
    cy.get('svg.sa-icon').should('have.class', 'sa-icon--xl')
  })
})
