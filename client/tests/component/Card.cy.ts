import Card from '@/components/common/Card.vue'

describe('Card', () => {
  it('renders slot content', () => {
    cy.mount(Card, { slots: { default: '<p>Study A</p>' } })
    cy.contains('p', 'Study A').should('exist')
  })

  it('renders within a sa-card container', () => {
    cy.mount(Card, { slots: { default: 'Content' } })
    cy.get('.sa-card').should('contain.text', 'Content')
  })
})
