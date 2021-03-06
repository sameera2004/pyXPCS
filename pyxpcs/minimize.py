from array import *
#from scipy import *
from scipy.optimize import leastsq
import scipy.io.array_import
from scipy import factorial
from numpy import *
import  matplotlib.pylab as pyl

def residuals(p,y,x,yerr):
   err = (y-peval(x,p))/yerr
   return err
#########################################################
def residuals_duri_global(p, y, x,yerr,qval): 
        print p
#not the squared ones, squaring will be handled by leastsq
        err = 0
        xplot=pyl.array(x,typecode='d')
        for i,q in enumerate(qval):
           q= float(q)
           y_calc=peval_duri_global(x,p,q)
#           y_calcplot=pyl.array(y_calc,typecode='d')
           err+=(y[i,:]-y_calc)**2
#           err+=y[i,:]-y_calc
#           pyl.figure(2)
#           yplot=pyl.array(y[i,:],typecode='d')
#           pyl.subplot(211)
#           pyl.semilogx(xplot,y_calcplot-yplot,'-')
#           pyl.hold(False)
#           pyl.subplot(212)
#           pyl.semilogx(xplot,yplot,'o',xplot,y_calcplot,'-')
#           pyl.hold(False)
	err = sqrt(err) 
	return err

#########################################################
def peval_duri_global(x,p,q):
   global func
   return eval(func)
#########################################################
def peval(x,p):
   global func
   return eval(func)

#########################################################
def def_func(npar,c0):
   global func
   for i in range(npar):
      par_old='p'+str(i)
      par_new='p['+str(i)+']'
      func= func.replace(par_old,par_new)
   nconst=len(c0)
   for i in range(nconst):
      name='c'+str(i)
      value=str(c0[i])
      func=func.replace(name,value)
   print func
   return func

#########################################################
def fitting(x,y,f,p0,c0,yerr='none',qval='none'):
   if yerr=='none':
      yerr=y*0+y/y
   global func
   func=f
   npar=len(p0)
   func=def_func(npar,c0)
   print 'fitting with funcion: ', func
   print 'no of parameters: ', len(p0)
#   plsq = leastsq(residuals, p0, args=(y,x,yerr), col_deriv=1, maxfev=20000)
   if 'duri' in func:
      plsq= leastsq(residuals_duri_global, p0, args=(y,x,yerr,qval), col_deriv=0, ftol=1e-4, maxfev=2000000)
   else:
      plsq = leastsq(residuals, p0, args=(y,x,yerr), col_deriv=0, maxfev=20000)
   if npar==1:
      final_par = array([plsq[0]])
   else:
      final_par = plsq[0]
   if 'duri' in func:
      yfit=0*y
      for i,q in enumerate(qval):
         q=float(q)
         yfit[i,:]=pyl.array(peval_duri_global(x,final_par,q),typecode='d')
   else:
      yfit=pyl.array(peval(x,final_par),typecode='d')
   return yfit, final_par, func

def func_duri(x,q,gamma0,delta,alfa,n=101):
   gn=resize(0*x,[n,len(x)])
   alfa=abs(cos(alfa))
   for k in range(n):
       P_k=(exp(-abs(gamma0)*x)*(abs(gamma0)*x)**k)/factorial(k)
       gn[k,:]= P_k*exp(-(q*abs(delta)*k**abs(alfa))**2)
   g1=sum(gn,axis=0)
   return g1




#####from yuriy


 #out=leastsq(errfunc,p0,args=(xdata,ydata,b),full_output=1)
 #   p1[i,1:]=out[0]
  #  covar=out[1]
   # err[i,:]=sqrt(diag(covar,k=0))

