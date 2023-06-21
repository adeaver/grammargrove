import Header from '../../components/Header';

import LoginComponent from './LoginComponent';

const IndexPage = () => {
    return (
        <div>
            <Header />
            <div class='w-full h-screen'>
                <LoginComponent />
            </div>
        </div>
    )
}

export default IndexPage;
