import DropdownMenu from '@/components/common/DropdownMenu.vue'

describe('DropdownMenu', () => {
  it('does not render when closed', () => {
    cy.mount(DropdownMenu, { props: { open: false }, slots: { default: 'Item' } })
    cy.get('.sa-dropdown-menu').should('not.exist')
  })

  it('renders slot content when open', () => {
    cy.mount(DropdownMenu, { props: { open: true }, slots: { default: 'Item' } })
    cy.get('.sa-dropdown-menu').should('be.visible').and('contain.text', 'Item')
  })

  it('emits update:open false when clicking outside the menu', () => {
    const onUpdateOpen = cy.stub().as('onUpdateOpen')
    cy.mount(DropdownMenu, {
      props: { open: true },
      attrs: { 'onUpdate:open': onUpdateOpen },
      slots: { default: 'Item' },
    })
    cy.get('body').click(0, 0, { force: true })
    cy.get('@onUpdateOpen').should('have.been.calledWith', false)
  })

  it('does not close when clicking inside the menu', () => {
    const onUpdateOpen = cy.stub().as('onUpdateOpen')
    cy.mount(DropdownMenu, {
      props: { open: true },
      attrs: { 'onUpdate:open': onUpdateOpen },
      slots: { default: '<p>Item</p>' },
    })
    cy.get('.sa-dropdown-menu p').click()
    cy.get('@onUpdateOpen').should('not.have.been.called')
  })
})
