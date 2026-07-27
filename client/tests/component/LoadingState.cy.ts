import LoadingState from '@/components/common/LoadingState.vue'

describe('LoadingState', () => {
  it('renders the message', () => {
    cy.mount(LoadingState, { props: { message: 'Loading Holdings' } })
    cy.get('.sa-loading-state').should('contain.text', 'Loading Holdings')
  })

  it('cycles the trailing dots without moving the message', () => {
    cy.clock()
    cy.mount(LoadingState, { props: { message: 'Loading Holdings' } })

    cy.get('.sa-loading-state__dots').should('have.text', '.')
    cy.tick(500)
    cy.get('.sa-loading-state__dots').should('have.text', '..')
    cy.tick(500)
    cy.get('.sa-loading-state__dots').should('have.text', '...')
    cy.tick(500)
    cy.get('.sa-loading-state__dots').should('have.text', '.')
  })
})
