import EmptyState from '@/components/common/EmptyState.vue'

describe('EmptyState', () => {
  it('renders the message', () => {
    cy.mount(EmptyState, { props: { message: 'No holdings yet.' } })
    cy.get('.sa-empty-state').should('have.text', 'No holdings yet.')
  })
})
