import TopBar from '@/components/common/TopBar.vue'

describe('TopBar', () => {
  it('renders the title', () => {
    cy.mount(TopBar)
    cy.get('h1').should('contain.text', 'Stock Analyzer')
  })

  it('opens the dropdown menu when the hamburger button is clicked', () => {
    cy.mount(TopBar)
    cy.get('.sa-dropdown-menu').should('not.exist')
    cy.get('.sa-top-bar__menu-button').click()
    cy.get('.sa-dropdown-menu').should('be.visible').and('contain.text', 'Log out')
  })

  it('emits logout and closes the menu when "Log out" is clicked', () => {
    const onLogout = cy.stub().as('onLogout')
    cy.mount(TopBar, { attrs: { onLogout } })
    cy.get('.sa-top-bar__menu-button').click()
    cy.contains('.sa-dropdown-item', 'Log out').click()
    cy.get('@onLogout').should('have.been.calledOnce')
    cy.get('.sa-dropdown-menu').should('not.exist')
  })
})
