class MathUtils:
    @staticmethod
    def forwardDifferences(n, x, x_df, x_d2f, x_d3f, y, y_df, y_d2f, y_d3f, z, z_df, z_d2f, z_d3f):
        points = [(float(x), float(y), float(z))]
        
        for _ in range(n-1):
            x += x_df
            x_df += x_d2f
            x_d2f += x_d3f
            y += y_df
            y_df += y_d2f
            y_d2f += y_d3f
            z += z_df
            z_df += z_d2f
            z_d2f += z_d3f
            points.append((float(x), float(y), float(z)))
        return points