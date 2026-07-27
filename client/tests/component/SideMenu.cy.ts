import SideMenu from '@/components/common/SideMenu.vue'

describe('SideMenu', () => {
  it('renders the title', () => {
    cy.mount(SideMenu, { props: { title: 'Existing Studies' } })
    cy.get('h2').should('contain.text', 'Existing Studies')
  })

  it('renders slot content', () => {
    cy.mount(SideMenu, {
      props: { title: 'Existing Studies' },
      slots: { default: '<p>Study A</p>' },
    })
    cy.contains('p', 'Study A').should('exist')
  })

  it('defaults to size m', () => {
    cy.mount(SideMenu, { props: { title: 'Existing Studies' } })
    cy.get('.sa-side-menu').should('have.class', 'sa-side-menu--m')
  })

  it('applies the requested size class', () => {
    cy.mount(SideMenu, { props: { title: 'Existing Studies', size: 'l' } })
    cy.get('.sa-side-menu').should('have.class', 'sa-side-menu--l')
  })
})
