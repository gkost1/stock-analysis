import Button from '@/components/common/Button.vue'

describe('Button', () => {
  it('renders slot content', () => {
    cy.mount(Button, { slots: { default: 'Click me' } })
    cy.get('button').should('contain.text', 'Click me')
  })

  it('emits click when clicked', () => {
    const onClick = cy.stub().as('onClick')
    cy.mount(Button, {
      slots: { default: 'Click me' },
      attrs: { onClick },
    })
    cy.get('button').click()
    cy.get('@onClick').should('have.been.calledOnce')
  })
})
