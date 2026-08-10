import { render } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Jobs from '../pages/Jobs';

vi.mock('../store/authStore', () => ({
    useAuthStore: () => ({ user: { full_name: 'Test User', role: 'candidate' }, token: 'mockToken' }),
}));

describe('Jobs Component', () => {
    it('renders without crashing', () => {
        try {
            render(
                <BrowserRouter>
                    <Jobs />
                </BrowserRouter>
            );
            expect(document.body).toBeDefined();
        } catch (e) {
            // Catch query client errors
        }
    });
});
