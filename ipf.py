import numpy as np

__author__ = 'Paul Tune'


class IPF:
    """
    Iterative proportional fitting: scales a non-negative matrix according to
    row and column sum constraints. Requires Numpy.
    """
    def l1_error(self, mtx, rowsum, colsum):
        """
        L1 error criterion. Used to compute the termination criterion of
        IPF.

        :param mtx: input non-negative matrix
        :param rowsum: row sum constraints
        :param colsum: column sum constraints
        :return:
        """
        rtol = abs(rowsum - mtx.sum(1))
        ctol = abs(colsum - mtx.sum(0))

        return rtol.sum() + ctol.sum()

    def run(self, mtx, rowsum, colsum, tol=1e-3, maxiter=100):
        """
        Run Iterative Proportional Fitting algorithm on a non-negative matrix
        with specified row and column sum constraints. Requires Numpy.

        :param mtx: input non-negative matrix
        :param rowsum: row sum constraints
        :param colsum: column sum constraints
        :param tol: (optional) tolerance parameter (default: 1e-3)
        :param maxiter: (optional) maximum number of iterations (default: 100)
        :return:
        """
        if len(mtx) == 0:
            print("Empty matrix")
            return

        m = mtx.shape[0]
        n = mtx.shape[1]

        # sanity checks
        if rowsum.shape[0] != m:
            print("Row sum constraints do not match number of columns in A")
            return

        if colsum.shape[1] != n:
            print("Column sum constraints do not match number of rows in A")
            return

        if rowsum.min() < 0:
            print("Row sum constraints must be non-negative")
            return

        if colsum.min() < 0:
            print("Column sum constraints must be non-negative")
            return

        if mtx.min() < 0:
            print("Input matrix must be non-negative")
            return

        iteration = 0
        while iteration < maxiter:
            # essentially L1 tolerance criterion
            if self.l1_error(mtx, rowsum, colsum) < tol:
                print('Tolerance criterion reached')
                break

            for i in range(m):
                # always remember to update the row and column sums
                # row sum of scaled matrix
                current_row_sum = mtx.sum(1)
                # column sum of scaled matrix
                current_col_sum = mtx.sum(0)

                for j in range(n):
                    # scale rows
                    mtx[i, j] = float(rowsum[i, 0])*mtx[i, j]/current_row_sum[i, 0]
                    mtx[i, j] = float(rowsum[i, 0])*mtx[i, j]/current_row_sum[i, 0]

                    # scale columns
                    mtx[i, j] = float(colsum[0, j])*mtx[i, j]/current_col_sum[0, j]

            iteration += 1

        if iteration > maxiter:
            print('Maximum number of iterations exceeded')

        return


if __name__ == '__main__':
    print('Test IPF')

    A = np.matrix('1.0 2 3;  4 5 6; 7 8 9')
    r = np.matrix('1.0; 1.0; 1.0')
    c = np.matrix('1.0 1.0 1.0')
    t = np.matrix('0; 1; 0')

    print('Initial matrix')
    print(A)

    ipf = IPF()
    ipf.run(A, r, c)

    print('\n')
    print('Final matrix')
    print(A)

    print('\n')
    print('L1 error at termination')
    print(ipf.l1_error(A, r, c))