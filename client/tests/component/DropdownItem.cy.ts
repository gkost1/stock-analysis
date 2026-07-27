import DropdownItem from '@/components/common/DropdownItem.vue'

describe('DropdownItem', () => {
  it('renders slot content', () => {
    cy.mount(DropdownItem, { slots: { default: 'Log out' } })
    cy.get('button').should('contain.text', 'Log out')
  })

  it('emits click when clicked', () => {
    const onClick = cy.stub().as('onClick')
    cy.mount(DropdownItem, {
      slots: { default: 'Log out' },
      attrs: { onClick },
    })
    cy.get('button').click()
    cy.get('@onClick').should('have.been.calledOnce')
  })
})
