import { mount } from '@vue/test-utils'
import FolderPage from '@/views/FolderPage.vue'
import { describe, expect, test } from 'vitest'
import { createTestingPinia } from '@pinia/testing'
import { useMainStore } from '@/store'
import Auth from '@/views/Auth.vue'

describe('FolderPage.vue', () => {
  test('renders folder view', () => {
    const mockRoute = {
      params: {
        id: 'Outbox'
      }
    }
    const wrapper = mount(FolderPage, {
      global: {
        mocks: {
          $route: mockRoute
        }
      }
    })
    expect(wrapper.text()).toMatch('Explore UI Components')
  })
})

describe('Auth.vue', () => {
  it('renders properly', () => {
    const wrapper = mount(Auth, {
      global: {
        plugins: [createTestingPinia()]
      }
    })
    expect(wrapper.exists()).toBe(true)
  })

  it('handles login form submission', async () => {
    const wrapper = mount(Auth, {
      global: {
        plugins: [createTestingPinia()]
      }
    })
    
    const store = useMainStore()
    await wrapper.find('form').trigger('submit')
    expect(store.setAuth).toHaveBeenCalled()
  })
})
